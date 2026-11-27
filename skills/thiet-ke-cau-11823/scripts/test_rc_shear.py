"""Test rc_shear.py — đối chiếu tính tay từ phương trình đã phiên (tr.24-25, 59-72).

Run:  python3 -m unittest discover -s skills/thiet-ke-cau-11823/scripts
"""
import math
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rc_shear as rcs      # noqa: E402
import rc_flexure as rcf    # noqa: E402


class VatLieu42(unittest.TestCase):
    # Điều 4.2.4 pt (8) tr.24
    def test_ec_pt8(self):
        self.assertAlmostEqual(rcs.ec(35, 2400), 0.0017 * 2400**2 * 35**0.33, places=6)

    def test_ec_guard(self):
        with self.assertRaises(rcs.ValueRange):
            rcs.ec(35, 1200)          # wc ngoài 1440–2500
        with self.assertRaises(rcs.ValueRange):
            rcs.ec(120)               # f'c > 105

    # Điều 4.2.6 tr.25 — các hệ số bản in
    def test_fr_he_so(self):
        fpc = 50.0
        self.assertAlmostEqual(rcs.fr_flexure(fpc), 0.63 * math.sqrt(fpc))
        self.assertAlmostEqual(rcs.fr_flexure(fpc, for_mcre_8343=True), 0.52 * math.sqrt(fpc))
        self.assertAlmostEqual(rcs.fr_flexure(fpc, "sand"), 0.52 * math.sqrt(fpc))
        self.assertAlmostEqual(rcs.fr_flexure(fpc, "all"), 0.45 * math.sqrt(fpc))


class CauTao82(unittest.TestCase):
    def test_tau_u_pt70(self):
        # Vu=600 kN, φ=0.9, Vp=0, bv=300, dv=700
        tau = rcs.tau_u(600e3, 0.0, 300, 700)
        self.assertAlmostEqual(tau, (600e3 / 0.9) / (300 * 700), places=6)

    def test_smax_pt6869(self):
        # νu < 0,125√f'c → min(0,8dv, 600); νu ≥ → min(0,4dv, 300)  (tr.61)
        self.assertEqual(rcs.s_max(700, 0.5, 50.0), 560.0)        # 0,8·700=560
        self.assertEqual(rcs.s_max(800, 0.5, 50.0), 600.0)        # chặn 600
        self.assertEqual(rcs.s_max(700, 1.0, 50.0), 280.0)        # 1,0 ≥ 0,125√50=0,884
        self.assertEqual(rcs.s_max(900, 1.0, 50.0), 300.0)        # chặn 300

    def test_av_min_pt66(self):
        # Av ≥ 0,083·bv·s·√f'c/fy  (tr.60)
        got = rcs.av_min(300, 150, 35.0, 420)
        self.assertAlmostEqual(got, 0.083 * 300 * 150 * math.sqrt(35) / 420, places=6)

    def test_av_min_hop_phan_doan_pt67(self):
        got = rcs.av_min(300, 150, 35.0, 420, segmental_box=True, bw=140)
        self.assertAlmostEqual(got, 0.35 * 140 * 150 / 420, places=6)


class DonGian8341(unittest.TestCase):
    # Số liệu: f'c=35, bv=300, dv=700, Av=200mm² (2Ø13?), fy=420, s=150
    FC, BV, DV, AV, FY, S = 35.0, 300, 700, 200.0, 420, 150

    def test_vc_pt74_beta2(self):
        vc = rcs.vc_general(2.0, self.FC, self.BV, self.DV)
        self.assertAlmostEqual(vc, 0.083 * 2.0 * math.sqrt(35) * 300 * 700, places=0)

    def test_vs_pt75_45do(self):
        vs = rcs.vs_steel(self.AV, self.FY, self.DV, self.S, 45.0)
        self.assertAlmostEqual(vs, 200 * 420 * 700 / 150, places=0)

    def test_full_simple_bam_trần_pt73(self):
        r = rcs.shear_simple(self.FC, self.BV, self.DV, self.AV, self.FY, self.S,
                             Vu=250e3)
        cap = 0.25 * math.sqrt(35) * 300 * 700
        self.assertAlmostEqual(r.cap, cap, places=0)
        self.assertAlmostEqual(r.Vn, min(r.Vc + r.Vs, cap), places=0)
        self.assertAlmostEqual(r.Vr, 0.9 * r.Vn, places=0)
        self.assertGreaterEqual(r.Vr, 250e3)

    def test_simple_can_av_min(self):
        with self.assertRaises(rcs.ValueRange):
            rcs.shear_simple(self.FC, self.BV, self.DV, 10.0, self.FY, self.S, Vu=250e3)


class TongQuatA(unittest.TestCase):
    def test_beta_pt77_theta_pt79(self):
        eps = 0.001
        r = rcs.general_a(eps, 50.0, 300, 700, 300.0, 420, 150, Vu=400e3)
        self.assertAlmostEqual(r.beta, 4.8 / (1 + 750 * eps), places=6)
        self.assertAlmostEqual(r.theta, 29 + 3500 * eps, places=6)  # 32.5 độ

    def test_sxe_pt78_chan(self):
        # không đủ đai min → pt (78); Sxe chặn [294, 2000]
        beta = rcs._beta_no_min(0.001, 50.0, 300, 700, ag=19.0, sx=700)
        sxe = min(max(35 * 700 / (19 + 16), 294), 2000)
        self.assertAlmostEqual(beta, 4.8 / (1 + 0.75) * 51 / (39 + sxe), places=6)

    def test_eps_guard(self):
        with self.assertRaises(rcs.ValueRange):
            rcs.general_a(0.007, 50.0, 300, 700, 300.0, 420, 150, Vu=400e3)
        with self.assertRaises(rcs.ValueRange):
            rcs.general_a(-0.001, 50.0, 300, 700, 300.0, 420, 150, Vu=400e3)


class BangCot4(unittest.TestCase):
    def test_o_goc(self):
        # hàng ≤0,075 cột εx·1000 ≤ −0,20 → θ=22,3 β=6,32 (đúng ô đầu ảnh in)
        theta, beta = rcs.table4(0.070, -0.0005)
        self.assertEqual((theta, beta), (22.3, 6.32))

    def test_o_giua(self):
        # hàng ≤0,125, εx·1000 = 0,10 ∈ cột ≤0,125 → θ=25,9 β=2,74
        theta, beta = rcs.table4(0.120, 0.0001)
        self.assertEqual((theta, beta), (25.9, 2.74))

    def test_ngoai_bang(self):
        with self.assertRaises(rcs.ValueRange):
            rcs.table4(0.30, 0.0001)      # Vu/f'c > 0,25
        with self.assertRaises(rcs.ValueRange):
            rcs.table4(0.10, 0.002)       # εx·1000 = 2 > 1,0


class DonGianHoa8343(unittest.TestCase):
    # Dầm DƯL: f'c=50, bv=180, dv=900, Av=200, fy=420, s=200
    # Vd=120kN, Vi=380kN, Mmax=520kN·m, Sc=Snc=3.6e6 mm³, Mdnc=210kN·m,
    # fcpe=6,5 MPa (nén dương), fpc=9,2 MPa
    def _run(self):
        return rcs.shear_simplified(50.0, 180, 900, 200.0, 420, 200,
                                    Vd=120e3, Vi=380e3, Mmax=520e6,
                                    Sc=3.6e6, Snc=3.6e6, Mdnc=210e6,
                                    fcpe=6.5, fpc_core=9.2)

    def test_mcre_pt87(self):
        r = self._run()
        fr = 0.52 * math.sqrt(50)
        self.assertAlmostEqual(r.Mcre, 3.6e6 * (fr + 6.5 + 210e6 / 3.6e6), places=0)

    def test_vci_cap_pt86(self):
        r = self._run()
        cap = 0.16 * math.sqrt(50) * 180 * 900
        self.assertLessEqual(r.Vci, cap + 1e-6)

    def test_vcw_pt88(self):
        r = self._run()
        vcw = (0.16 * math.sqrt(50) + 2.09 * 9.2) * 180 * 900
        self.assertAlmostEqual(r.Vcw, vcw, places=0)

    def test_quyet_dinh_va_cot_theta(self):
        r = self._run()
        self.assertIn(r.governing, ("Vci", "Vcw"))
        self.assertAlmostEqual(r.Vc, min(r.Vci, r.Vcw), places=6)
        if r.governing == "Vcw":
            self.assertEqual(r.cot_theta, 1.0)


class Mcr733(unittest.TestCase):
    def test_mcr_nguyen_khoi(self):
        # Snc=None → số hạng Mdnc triệt tiêu; fr=0,63√f'c (Điều 4.2.6 chung)
        fr = 0.63 * math.sqrt(35)
        got = rcf.mcr(35.0, Sc=2.4e6, Mdnc=50e6, gamma3="A615-420")
        self.assertAlmostEqual(got, 0.67 * (1.6 * fr) * 2.4e6, places=0)

    def test_mcr_co_lech_tiet_dien(self):
        fr = 0.63 * math.sqrt(40)
        got = rcf.mcr(40.0, Sc=3.0e6, Mdnc=100e6, Snc=2.0e6, fcpe=5.0,
                      gamma1="precast", gamma2="unbonded", gamma3="PS")
        want = 1.0 * ((1.2 * fr + 1.0 * 5.0) * 3.0e6 - 100e6 * (3.0e6 / 2.0e6 - 1))
        self.assertAlmostEqual(got, want, places=0)

    def test_phai_chon_gamma3(self):
        with self.assertRaises(rcf.ValueRange):
            rcf.mcr(35.0, 1e6, 1e6)      # mặc định cast-in-place-A → chặn

    def test_asmin_nguong(self):
        self.assertEqual(rcf.as_min_required(100e6, 150e6), 133e6)   # 1,33Mu nhỏ hơn
        self.assertEqual(rcf.as_min_required(120e6, 150e6), 150e6)   # Mcr nhỏ hơn


if __name__ == "__main__":
    unittest.main()
