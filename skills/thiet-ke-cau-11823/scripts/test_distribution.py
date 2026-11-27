"""Tests for distribution.py against hand calculations from references/phan-4-phan-bo.md.

Run:  python3 -m unittest discover -s skills/thiet-ke-cau-11823/scripts
"""
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import distribution as d  # noqa: E402


class CoreHelpers(unittest.TestCase):
    def test_kg(self):
        # Kg = n(I + A*eg^2) = 1.0*(2e11 + 6e5*800^2) — art 6.2.2.1, eq (14), tr.38
        self.assertAlmostEqual(d.kg(1.0, 2.0e11, 6.0e5, 800), 5.84e11)

    def test_lever_rule(self):
        # S=2400, de=600: wheel 1 lands on the exterior girder (600-de=0),
        # wheel 2 at 1800 mm -> reaction 0.5*(1-0) + 0.5*(1-1800/2400) = 0.625, x m=1.20
        self.assertAlmostEqual(d.lever_rule_exterior(2400, 600), 0.75)

    def test_lever_rule_interior(self):
        # S=2400: 0.5 + 0.5*(1-1800/2400) = 0.625 = 1500/2400 -> x m=1.20
        self.assertAlmostEqual(d.lever_rule_interior(2400), 0.75)

    def test_check_range_edges_inclusive(self):
        d.check_range("S", 1100, 1100, 4900, "Bảng 6")
        d.check_range("S", 4900, 1100, 4900, "Bảng 6")

    def test_check_range_rejects(self):
        with self.assertRaisesRegex(d.OutOfRange, "S"):
            d.check_range("S", 5000, 1100, 4900, "Bảng 6")


class InteriorMoment(unittest.TestCase):
    P = dict(S=2400, L=30000, ts=200, Kg=5e11, Nb=5)

    # Bảng 6, tr.44 — hàng a/e/k (i, j nếu liên kết đủ làm việc như một khối)
    def test_aek(self):
        r = d.moment_interior("k", **self.P)
        self.assertAlmostEqual(r.parts["1 làn"], 0.459485, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.654671, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    def test_aek_edges(self):  # mép phạm vi S phải được tính, không bị từ chối
        d.moment_interior("k", **{**self.P, "S": 1100})
        d.moment_interior("k", **{**self.P, "S": 4900})

    def test_aek_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.moment_interior("k", **{**self.P, "L": 80000})

    def test_aek_three_girders(self):  # Nb = 3: max(công thức, đòn bẩy) — Bảng 6, tr.44
        r = d.moment_interior("k", **{**self.P, "Nb": 3})
        self.assertAlmostEqual(r.g, max(0.654671, d.lever_rule_interior(2400)), places=5)
        self.assertEqual(r.governing, "đòn bẩy")

    def test_ij_use_aek_formulas(self):
        r = d.moment_interior("i", **self.P)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.654671, places=5)

    def test_missing_param_names_it(self):
        with self.assertRaisesRegex(TypeError, "Kg"):
            d.moment_interior("k", S=2400, L=30000, ts=200, Nb=5)

    # Bảng 6, tr.44 — hàng d (hộp bê tông nhiều ngăn đúc tại chỗ)
    def test_d(self):
        r = d.moment_interior("d", S=3000, L=30000, Nc=5)
        self.assertAlmostEqual(r.parts["1 làn"], 0.432989, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.706097, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    def test_d_nc_capped_at_8(self):  # "Nếu N0 > 8, dùng N0 = 8" (nghi N0/Nc) — Bảng 6, tr.44
        r12 = d.moment_interior("d", S=3000, L=30000, Nc=12)
        r8 = d.moment_interior("d", S=3000, L=30000, Nc=8)
        self.assertAlmostEqual(r12.g, r8.g, places=12)

    def test_d_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.moment_interior("d", S=4500, L=30000, Nc=5)

    # Bảng 6, tr.44 — hàng b/c (mặt bê tông trên dầm hộp bê tông khoảng rỗng)
    def test_bc(self):
        r = d.moment_interior("c", S=2500, L=30000, d=1000, Nb=4)
        self.assertAlmostEqual(r.parts["1 làn"], 0.326993, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.564903, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    def test_bc_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.moment_interior("b", S=2500, L=30000, d=2000, Nb=4)

    def test_bc_wide_spacing_lever_rule(self):  # S >= 5500: nguyên tắc đơn bẩy — Bảng 6, tr.44
        r = d.moment_interior("b", S=6000, L=30000, d=1000, Nb=4)
        self.assertAlmostEqual(r.g, 1.02, places=5)
        self.assertEqual(r.governing, "đòn bẩy")

    # Bảng 6, tr.44–45 — hàng f/g (dầm hộp bê tông đúc sẵn trong mặt cầu nhiều dầm)
    def test_fg(self):
        r = d.moment_interior("g", b=1200, L=30000, I=2e11, J=1e10, Nb=6)
        self.assertAlmostEqual(r.parts["1 làn"], 0.441589, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.362914, places=5)
        self.assertEqual(r.governing, "1 làn")

    def test_fg_k_floored_at_1_5(self):  # k = 2,5·Nb^-0,2 >= 1,5 — Bảng 6, tr.45
        r = d.moment_interior("f", b=1200, L=30000, I=2e11, J=1e10, Nb=20)
        self.assertAlmostEqual(r.parts["1 làn"], 0.379140, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.311592, places=5)

    def test_fg_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.moment_interior("f", b=1200, L=45000, I=2e11, J=1e10, Nb=6)

    # Bảng 6, tr.45 — hàng h (g = S/D, số làn chịu tải bất kỳ)
    def test_h_sd(self):
        r = d.moment_interior("h", S=2400, L=30000, W=9000, NL=3, I=2e11, J=1e10, mu=0.2)
        self.assertAlmostEqual(r.parts["S/D"], 0.755159, places=5)
        self.assertEqual(r.governing, "S/D")

    def test_h_out_of_range(self):  # NL <= 6
        with self.assertRaises(d.OutOfRange):
            d.moment_interior("h", S=2400, L=30000, W=9000, NL=7, I=2e11, J=1e10, mu=0.2)

    # Bảng 6, tr.46 — mảng bản thép trên dầm thép (loại a)
    def test_steel_grid(self):
        r = d.moment_interior("steel-grid", S=1500, tg=80)
        self.assertAlmostEqual(r.parts["1 làn"], 0.652174, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.625, places=5)
        self.assertEqual(r.governing, "1 làn")

    def test_steel_grid_thick_deck(self):  # Tg >= 100; 1 làn chỉ tới S <= 1800 — tr.46
        r = d.moment_interior("steel-grid", S=2500, tg=120)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.819672, places=5)
        self.assertNotIn("1 làn", r.parts)
        self.assertEqual(r.governing, "≥2 làn")

    def test_steel_grid_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.moment_interior("steel-grid", S=4000, tg=80)

    # Bảng 6, tr.46 — mặt cầu bê tông trên nhiều dầm hộp thép (loại b, c)
    def test_steel_box(self):
        r = d.moment_interior("steel-box", NL=3, Nb=5)
        self.assertAlmostEqual(r.g, 0.701667, places=5)
        self.assertEqual(r.governing, "bất kỳ làn")

    def test_steel_box_out_of_range(self):  # 0,5 <= NL/Nb <= 1,5
        with self.assertRaises(d.OutOfRange):
            d.moment_interior("steel-box", NL=3, Nb=7)

    # Bảng 7, tr.46 — mặt cầu tấm thép lượn sóng (Điều 6.2.2.2.2)
    def test_corrugated(self):
        r = d.moment_interior("corrugated", S=1500, tg=80)
        self.assertAlmostEqual(r.parts["1 làn"], 0.535714, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.555556, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    def test_corrugated_out_of_range(self):  # S <= 1700; Tg >= 50
        with self.assertRaises(d.OutOfRange):
            d.moment_interior("corrugated", S=2000, tg=80)
        with self.assertRaises(d.OutOfRange):
            d.moment_interior("corrugated", S=1500, tg=40)


if __name__ == "__main__":
    unittest.main()
