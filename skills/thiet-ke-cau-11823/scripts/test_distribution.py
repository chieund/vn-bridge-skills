"""Kiểm tra distribution.py đối chiếu tính tay từ references/phan-4-phan-bo.md.

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
        # Kg = n(I + A*eg^2) = 1.0*(2e11 + 6e5*800^2) — Điều 6.2.2.1, phương trình (14), tr.38
        self.assertAlmostEqual(d.kg(1.0, 2.0e11, 6.0e5, 800), 5.84e11)

    def test_lever_rule(self):
        # S=2400, de=600: bánh 1 rơi đúng lên dầm biên (600-de=0),
        # bánh 2 cách 1800 mm -> phản lực 0.5*(1-0) + 0.5*(1-1800/2400) = 0.625, nhân m=1.20
        self.assertAlmostEqual(d.lever_rule_exterior(2400, 600), 0.75)

    def test_lever_rule_interior(self):
        # S=2400: 0.5 + 0.5*(1-1800/2400) = 0.625 = 1500/2400 -> nhân m=1.20
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


class ExteriorMoment(unittest.TestCase):
    P = dict(S=2400, L=30000, ts=200, Kg=5e11, Nb=5)

    # Bảng 8, tr.48 — hàng a/e/k: 1 làn đòn bẩy, >=2 làn e·g_trong (e = 0,77 + de/2800)
    def test_aek(self):
        r = d.moment_exterior("k", de=300, **self.P)
        self.assertAlmostEqual(r.parts["1 làn"], 0.6, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.574240, places=5)
        self.assertEqual(r.governing, "1 làn")
        self.assertEqual(r.clause, "Bảng 8, tr.48")

    def test_aek_de_edges(self):  # mép phạm vi de vẫn tính được
        d.moment_exterior("k", de=-300, **self.P)
        d.moment_exterior("k", de=1700, **self.P)

    def test_aek_de_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.moment_exterior("k", de=1800, **self.P)
        with self.assertRaises(d.OutOfRange):
            d.moment_exterior("k", de=-400, **self.P)

    def test_aek_g_int_override(self):  # truyền g_int -> không cần tham số dầm trong
        r = d.moment_exterior("k", S=2400, de=300, g_int=0.8)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.701714, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    # Bảng 8, tr.48 — hàng d: g = We/4300, phạm vi We <= S
    def test_d(self):
        r = d.moment_exterior("d", S=4000, We=3500)
        self.assertAlmostEqual(r.g, 0.813953, places=5)

    def test_d_we_gt_s(self):
        with self.assertRaises(d.OutOfRange):
            d.moment_exterior("d", S=3000, We=3500)

    # Bảng 8, tr.48 — hàng b/c: e = 0,97 + de/8700; S > 5500 -> đơn bẩy
    def test_bc(self):
        r = d.moment_exterior("c", S=3000, L=30000, d=1000, Nb=4, de=1000)
        self.assertAlmostEqual(r.parts["1 làn"], 0.84, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.699499, places=5)
        self.assertEqual(r.governing, "1 làn")

    def test_bc_wide_lever(self):
        r = d.moment_exterior("b", S=6000, L=30000, d=1000, Nb=4, de=1000)
        self.assertAlmostEqual(r.g, 1.02, places=5)
        self.assertEqual(r.governing, "đòn bẩy")

    def test_bc_de_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.moment_exterior("b", S=3000, L=30000, d=1000, Nb=4, de=1500)

    # Bảng 8, tr.48 — hàng f/g: e1 = 1,125 + d/9100; e2 = 1,04 + de/7600; de <= 600
    def test_fg(self):
        r = d.moment_exterior("g", b=1200, L=30000, I=2e11, J=1e10, Nb=6, de=600, d=1000)
        self.assertAlmostEqual(r.parts["1 làn"], 0.545314, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.406082, places=5)
        self.assertEqual(r.governing, "1 làn")

    def test_fg_de_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.moment_exterior("f", b=1200, L=30000, I=2e11, J=1e10, Nb=6, de=700, d=1000)

    # Bảng 8, tr.48 — hàng đòn bẩy và hàng "như Bảng 6"
    def test_h_lever(self):
        r = d.moment_exterior("h", S=2400, de=300)
        self.assertAlmostEqual(r.g, 0.6, places=5)
        self.assertEqual(r.governing, "đòn bẩy")

    def test_steel_grid_lever(self):
        r = d.moment_exterior("steel-grid", S=2400, de=600)
        self.assertAlmostEqual(r.g, 0.75, places=5)

    def test_steel_box_like_bang6(self):
        r = d.moment_exterior("steel-box", NL=3, Nb=5)
        self.assertAlmostEqual(r.g, 0.701667, places=5)
        self.assertIn("Bảng 6", r.clause)

    def test_corrugated_not_listed(self):  # Bảng 8 không có hàng -> ngoài phạm vi
        with self.assertRaises(d.OutOfRange):
            d.moment_exterior("corrugated", S=1500, tg=80, de=300)


class InteriorShear(unittest.TestCase):
    # Bảng 11, tr.51 — hàng a/e/k; Nb = 3 dùng đơn bẩy
    def test_aek(self):
        r = d.shear_interior("k", S=2400, L=30000, ts=200, Nb=5)
        self.assertAlmostEqual(r.parts["1 làn"], 0.675789, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.465479, places=5)
        self.assertEqual(r.governing, "1 làn")

    def test_aek_nb3_lever(self):
        r = d.shear_interior("k", S=2400, L=30000, ts=200, Nb=3)
        self.assertAlmostEqual(r.g, 0.75, places=5)
        self.assertEqual(r.governing, "đòn bẩy")

    def test_aek_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.shear_interior("a", S=5000, L=30000, ts=200, Nb=5)

    # Bảng 11, tr.51 — hàng d
    def test_d(self):
        r = d.shear_interior("d", S=3000, L=30000, d=1200, Nc=5)
        self.assertAlmostEqual(r.parts["1 làn"], 0.739673, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.958153, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    def test_d_out_of_range(self):  # 890 <= d <= 2800
        with self.assertRaises(d.OutOfRange):
            d.shear_interior("d", S=3000, L=30000, d=500, Nc=5)

    # Bảng 11, tr.51 — hàng b/c; S > 5500 -> đơn bẩy
    def test_bc(self):
        r = d.shear_interior("c", S=2500, L=30000, d=1000, Nb=4)
        self.assertAlmostEqual(r.parts["1 làn"], 0.631643, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.774273, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    def test_bc_wide_lever(self):
        r = d.shear_interior("b", S=6000, L=30000, d=1000, Nb=4)
        self.assertAlmostEqual(r.g, 1.02, places=5)
        self.assertEqual(r.governing, "đòn bẩy")

    # Bảng 11, tr.51 — hàng f/g
    def test_fg(self):
        r = d.shear_interior("g", b=1200, L=30000, I=2e11, J=1e10, Nb=6)
        self.assertAlmostEqual(r.parts["1 làn"], 0.501717, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.520123, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    def test_fg_ij_out_uses_moment(self):  # I/J ngoài phạm vi -> dùng g mô men (tr.50)
        p = dict(b=1200, L=30000, I=1e10, J=1e10, Nb=6)
        r = d.shear_interior("g", **p)
        m = d.moment_interior("g", **p)
        self.assertEqual(r.parts, m.parts)
        self.assertIn("g mô men", r.clause)

    # Bảng 11, tr.52 — đơn bẩy / như Bảng 6
    def test_h_lever(self):
        r = d.shear_interior("h", S=2400)
        self.assertAlmostEqual(r.g, 0.75, places=5)
        self.assertEqual(r.governing, "đòn bẩy")

    def test_corrugated_lever(self):  # S=1500: 1,20·max(0,5; 1-900/1500) = 0,6
        r = d.shear_interior("corrugated", S=1500)
        self.assertAlmostEqual(r.g, 0.6, places=5)

    def test_steel_box_like_bang6(self):
        r = d.shear_interior("steel-box", NL=3, Nb=5)
        self.assertAlmostEqual(r.g, 0.701667, places=5)


class ExteriorShear(unittest.TestCase):
    # Bảng 12, tr.53 — hàng a/e/k: e = 0,6 + de/3000; Nb = 3 -> đơn bẩy
    def test_aek(self):
        r = d.shear_exterior("k", S=2400, L=30000, ts=200, Nb=5, de=300)
        self.assertAlmostEqual(r.parts["1 làn"], 0.6, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.325836, places=5)
        self.assertEqual(r.governing, "1 làn")

    def test_aek_nb3_lever(self):
        r = d.shear_exterior("k", S=2400, L=30000, ts=200, Nb=3, de=300)
        self.assertEqual(r.governing, "đòn bẩy")
        self.assertAlmostEqual(r.g, 0.6, places=5)

    def test_aek_de_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.shear_exterior("k", S=2400, L=30000, ts=200, Nb=5, de=1800)

    # Bảng 12, tr.53 — hàng d: e = 0,64 + de/3800, -600 <= de <= 1500
    def test_d(self):
        r = d.shear_exterior("d", S=3000, L=30000, d=1200, Nc=5, de=0)
        self.assertAlmostEqual(r.parts["1 làn"], 0.6, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.613218, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    def test_d_de_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.shear_exterior("d", S=3000, L=30000, d=1200, Nc=5, de=1600)

    # Bảng 12, tr.53 — hàng b/c: e = 0,8 + de/3050, 0 <= de <= 1400
    def test_bc(self):
        r = d.shear_exterior("c", S=2500, L=30000, d=1000, Nb=4, de=1000)
        self.assertAlmostEqual(r.parts["1 làn"], 0.768, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.873278, places=5)
        self.assertEqual(r.governing, "≥2 làn")

    def test_bc_de_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.shear_exterior("b", S=2500, L=30000, d=1000, Nb=4, de=1500)

    # Bảng 12, tr.53 — hàng f/g: e1 = 1,25 + de/6100; 300 <= de <= 600
    def test_fg(self):
        r = d.shear_exterior("g", b=1200, L=30000, I=2e11, J=1e10, Nb=6, de=300)
        self.assertAlmostEqual(r.parts["1 làn"], 0.651820, places=5)
        self.assertAlmostEqual(r.parts["≥2 làn"], 0.520123, places=5)
        self.assertEqual(r.governing, "1 làn")

    def test_fg_de_out_of_range(self):
        with self.assertRaises(d.OutOfRange):
            d.shear_exterior("f", b=1200, L=30000, I=2e11, J=1e10, Nb=6, de=200)

    def test_h_lever(self):
        r = d.shear_exterior("h", S=2400, de=300)
        self.assertAlmostEqual(r.g, 0.6, places=5)
        self.assertEqual(r.governing, "đòn bẩy")


class SkewFactors(unittest.TestCase):
    # Bảng 9, tr.49 — hàng a/e/k: 1 - c1·(tan θ)^1,5; θ<30 -> 1,0; θ>60 dùng 60
    def test_moment_aek(self):
        f = d.skew_moment("k", 45, S=2400, L=30000, Kg=5e11, tg=200, Nb=5)
        self.assertAlmostEqual(f, 0.915048, places=5)

    def test_moment_aek_below_30(self):
        self.assertEqual(d.skew_moment("k", 20, S=2400, L=30000, Kg=5e11, tg=200, Nb=5), 1.0)

    def test_moment_aek_clamped_at_60(self):
        kw = dict(S=2400, L=30000, Kg=5e11, tg=200, Nb=5)
        self.assertEqual(d.skew_moment("k", 70, **kw), d.skew_moment("k", 60, **kw))

    def test_moment_aek_requires_four_girders(self):  # phạm vi Bảng 9: Nb >= 4
        with self.assertRaises(d.OutOfRange):
            d.skew_moment("k", 45, S=2400, L=30000, Kg=5e11, tg=200, Nb=3)

    # Bảng 9, tr.49 — hàng b/c/f/g: 1,05 - 0,25·tan θ <= 1,0
    def test_moment_bc(self):
        self.assertAlmostEqual(d.skew_moment("b", 45), 0.8, places=5)
        self.assertEqual(d.skew_moment("b", 0), 1.0)

    def test_moment_no_row(self):
        with self.assertRaises(d.OutOfRange):
            d.skew_moment("h", 45)

    # Bảng 13, tr.54 — nhân vào g lực cắt tại góc tù
    def test_shear_aek(self):
        f = d.skew_shear("k", 30, S=2400, L=30000, ts=200, Kg=5e11, Nb=5)
        self.assertAlmostEqual(f, 1.092649, places=5)

    def test_shear_zero(self):
        f = d.skew_shear("k", 0, S=2400, L=30000, ts=200, Kg=5e11, Nb=5)
        self.assertEqual(f, 1.0)

    def test_shear_theta_out_of_range(self):  # Bảng 13 không kẹp -> raise
        with self.assertRaises(d.OutOfRange):
            d.skew_shear("k", 75, S=2400, L=30000, ts=200, Kg=5e11, Nb=5)

    def test_shear_d(self):
        f = d.skew_shear("d", 30, S=3000, L=30000, d=1200, Nb=4)
        self.assertAlmostEqual(f, 1.350534, places=5)

    def test_shear_bc(self):
        f = d.skew_shear("c", 30, S=2500, L=30000, d=1000, Nb=3)
        self.assertAlmostEqual(f, 1.210819, places=5)

    def test_shear_fg(self):  # f/g dùng sqrt(tan θ) — chỉ đúng với góc dương
        f = d.skew_shear("f", 45, L=30000, d=1000, b=1200, Nb=6)
        self.assertAlmostEqual(f, 1.333333, places=5)


class DeckAndSlab(unittest.TestCase):
    # Bảng 10, tr.50 — phần sổ tải trọng bánh xe cho dầm ngang (trục 145 kN)
    def test_stringer_concrete(self):
        self.assertAlmostEqual(d.stringer_wheel_share("concrete", 1500), 0.833333, places=5)

    def test_stringer_concrete_out(self):  # S <= 1800
        with self.assertRaises(d.OutOfRange):
            d.stringer_wheel_share("concrete", 1900)

    def test_stringer_grid_thin(self):  # Tg <= 100: S/1400, S <= 1500
        self.assertAlmostEqual(d.stringer_wheel_share("steel-grid", 1400, tg=80), 1.0, places=5)
        with self.assertRaises(d.OutOfRange):
            d.stringer_wheel_share("steel-grid", 1600, tg=80)

    def test_stringer_grid_thick(self):  # Tg > 100: S/1800, S <= 1800
        self.assertAlmostEqual(d.stringer_wheel_share("steel-grid", 1700, tg=120), 0.944444, places=5)

    def test_stringer_corrugated(self):  # S/1700, Tg >= 50
        self.assertAlmostEqual(d.stringer_wheel_share("corrugated", 1500, tg=80), 0.882353, places=5)
        with self.assertRaises(d.OutOfRange):
            d.stringer_wheel_share("corrugated", 1500, tg=40)

    def test_stringer_needs_tg(self):
        with self.assertRaises(TypeError):
            d.stringer_wheel_share("steel-grid", 1400)

    # Điều 6.2.3, tr.55-56 — bề rộng dải tương đương cầu bản (mm)
    def test_slab_one_lane(self):  # pt (17): E = 250 + 0,42·sqrt(L1·W1); W1 kẹp 9000
        self.assertAlmostEqual(d.slab_equiv_width(24000, 12000, 1), 5595.727266, places=5)

    def test_slab_multi(self):  # pt (18): E = 2100 + 0,12·sqrt(L1·W1) <= W/NL
        self.assertAlmostEqual(d.slab_equiv_width(24000, 12000, 3), 3863.632615, places=5)

    def test_slab_multi_capped(self):  # chặn W/NL = 9000/3 nhỏ hơn công thức
        self.assertAlmostEqual(d.slab_equiv_width(24000, 9000, 3), 3000.0, places=5)

    def test_slab_skew(self):  # pt (19): r = 1,05 - 0,25·tan θ <= 1,00
        self.assertAlmostEqual(d.slab_skew_factor(30), 0.905662, places=5)
        self.assertEqual(d.slab_skew_factor(0), 1.0)


if __name__ == "__main__":
    unittest.main()
