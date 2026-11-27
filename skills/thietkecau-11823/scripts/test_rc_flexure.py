"""Test rc_flexure.py đối chiếu tính tay từ các phương trình đã phiên (tr.40-44).

Run:  python3 -m unittest discover -s skills/thietkecau-11823/scripts
"""
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rc_flexure as rc  # noqa: E402


class HeSoVatLieu(unittest.TestCase):
    # Điều 7.2.2 tr.40 — α1, β1 theo f'c
    def test_alpha1_beta1_common(self):
        self.assertEqual(rc.alpha1(35), 0.85)
        self.assertAlmostEqual(rc.beta1(35), 0.80, places=6)   # 0,85 - 0,05·7/7
        self.assertEqual(rc.beta1(28), 0.85)

    def test_alpha1_beta1_high_and_floor(self):
        self.assertAlmostEqual(rc.alpha1(80), 0.8214286, places=5)
        self.assertEqual(rc.beta1(80), 0.65)                   # sàn theo bản in
        self.assertEqual(rc.alpha1(500), 0.75)                 # sàn α1

    # Điều 7.2.2 tr.39 — nội suy εcl, εtl theo fy
    def test_eps_limits(self):
        self.assertEqual(rc.eps_cl(None, True), 0.002)         # toàn bộ thép DƯL
        self.assertEqual(rc.eps_tl(420, False), 0.005)
        self.assertAlmostEqual(rc.eps_cl(550, False), 0.0029630, places=6)
        self.assertAlmostEqual(rc.eps_tl(600, False), 0.0064118, places=5)


class RcRectangle(unittest.TestCase):
    def test_basic(self):
        # b=400 d=700 As=4000 fc=35 fy=420 (N.mm): a=141,18; Mn=As·fy·(d−a/2)
        r = rc.flexure(35, 400, ds=700, As=4000, fy=420)
        self.assertAlmostEqual(r.a, 141.176, places=2)
        self.assertAlmostEqual(r.c, 176.471, places=2)
        self.assertAlmostEqual(r.Mn / 1e6, 1057.41, delta=0.05)
        self.assertAlmostEqual(r.eps_t, 0.0089, places=4)
        self.assertEqual(r.mode, "không khống chế kéo")
        self.assertAlmostEqual(r.phi, 0.90, places=6)          # pt (13) chặn trên 0,9
        self.assertAlmostEqual(r.Mr / 1e6, 951.67, delta=0.05)


class RcTee(unittest.TestCase):
    def test_flange_governs(self):
        # a <= hf -> như chữ nhật bề rộng b (7.3.2.3 tr.44: bw = b)
        r = rc.flexure(35, 200, ds=900, As=9000, fy=420, b=1200, hf=150)
        self.assertLessEqual(r.a, 150)
        self.assertAlmostEqual(r.Mn / 1e6, 3201.88, delta=0.05)
        self.assertAlmostEqual(r.phi, 0.90, places=6)

    def test_web_governs(self):
        # a > hf -> pt (32): thêm số hạng cánh thừa α1·f'c·(b−bw)·hf·(a/2−hf/2)
        r = rc.flexure(35, 200, ds=900, As=15000, fy=420, b=1200, hf=150)
        self.assertGreater(r.a, 150)
        self.assertAlmostEqual(r.c, 386.03, delta=0.5)
        self.assertAlmostEqual(r.Mn / 1e6, 5051.58, delta=0.5)
        # εt = 0,003994 giữa εcl=0,002 và εtl=0,005 -> nội suy pt (13)
        self.assertAlmostEqual(r.phi, 0.84971, places=4)
        self.assertEqual(r.mode, "chuyển tiếp (nội suy pt (12)/(13))")
        self.assertAlmostEqual(r.Mr / 1e6, 4292.4, delta=2.0)


class PtSections(unittest.TestCase):
    def test_bonded(self):
        # DƯL dính bám: pt (23)-(26); k = 2(1,04 − fpy/fpu) = 0,338065
        r = rc.flexure(35, 400, dp=900, Ap=1000, fpu=1860, fpy=1620)
        self.assertAlmostEqual(r.Mn / 1e6, 1433.38, delta=0.5)
        self.assertAlmostEqual(r.fps, 1732.8, delta=1.0)
        # DƯL không khống chế kéo: φ theo pt (12) — bản in cho tới 1,00 (⚠ tr.30)
        self.assertAlmostEqual(r.phi, 1.0, places=6)

    def test_unbonded(self):
        # fpe + 6300(dp−c)/λc vượt fpy -> chặn tại fpy (pt (27)); λc = 2·15000/3
        r = rc.flexure(35, 400, dp=900, Ap=1000, fpu=1860, fpy=1620,
                       fpe=1200, unbonded=True, lambda_i=15000, n_dev=1)
        self.assertAlmostEqual(r.c, 170.17, delta=0.5)
        self.assertAlmostEqual(r.fps, 1620.0, places=3)       # bị chặn fpy
        self.assertAlmostEqual(r.Mn / 1e6, 1347.74, delta=0.5)
        self.assertAlmostEqual(r.phi, 1.0, places=6)

    def test_fpe_low_flag(self):
        r = rc.flexure(35, 400, dp=900, Ap=1000, fpu=1860, fpy=1620, fpe=800,
                       unbonded=True, lambda_i=15000, n_dev=1)
        self.assertTrue(any("fpe < 0,5" in n for n in r.notes))  # điều kiện tr.40

    def test_mixed_np_pt_min_phi(self):
        # bản in tr.31: nhiều loại thép -> dùng φ nhỏ nhất theo từng loại
        r = rc.flexure(35, 400, ds=700, As=3000, fy=420, dp=900,
                       Ap=500, fpu=1860, fpy=1620)
        self.assertIn("nguồn φ:", " | ".join(r.notes))


class EdgeCases(unittest.TestCase):
    def test_compression_controlled_phi_floor(self):
        r = rc.flexure(35, 400, ds=300, As=4420, fy=420)
        self.assertAlmostEqual(r.phi, 0.75, places=6)          # cận dưới pt (13)
        self.assertEqual(r.mode, "khống chế nén")

    def test_inverted_section_rejected(self):
        # fs = fy vô nghiệm (trục trung hòa vượt ds) -> từ chối, yêu cầu tương thích biến dạng
        with self.assertRaises(rc.ValueRange):
            rc.flexure(35, 400, ds=250, As=6000, fy=420)

    def test_missing_inputs(self):
        with self.assertRaises(rc.ValueRange):
            rc.flexure(35, 400, As=1000)                        # thiếu ds/fy
        with self.assertRaises(rc.ValueRange):
            rc.flexure(35, 400, dp=900, Ap=100, fpu=1860, fpy=1620,
                       unbonded=True)                           # thiếu fpe/λi


if __name__ == "__main__":
    unittest.main()