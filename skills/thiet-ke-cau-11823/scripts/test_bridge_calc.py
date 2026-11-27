"""Tests for bridge_calc.py against hand calculations and the locked reference file.

Run:  python3 -m unittest discover -s skills/thiet-ke-cau-11823/scripts
"""
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bridge_calc as t  # noqa: E402

REFERENCE = (HERE.parent / "references" / "he-so-co-ban.md").read_text(encoding="utf-8")


class LockedCoefficientsMatchReference(unittest.TestCase):
    """If a coefficient changes in the script, the reference file must say the same."""

    def test_values(self):
        self.assertEqual(t.TRUCK_AXLES, (35.0, 145.0, 145.0))
        self.assertEqual(t.TANDEM_AXLES, (110.0, 110.0))
        self.assertEqual(t.LANE_LOAD, 9.3)
        self.assertEqual(t.IM, {"normal": 33.0, "fatigue": 15.0, "deck-joint": 75.0})
        self.assertEqual([t.multiple_presence_factor(n) for n in (1, 2, 3, 4, 6)],
                         [1.20, 1.00, 0.85, 0.65, 0.65])
        self.assertEqual(t.LIMIT_STATES["str1"]["ll"], 1.75)
        self.assertEqual(t.LIMIT_STATES["str1"]["dc"], (1.25, 0.90))
        self.assertEqual(t.LIMIT_STATES["str1"]["dw"], (1.50, 0.65))
        self.assertEqual(t.DEFLECTION_LIMITS, {"vehicle": 800, "pedestrian": 1000})

    def test_reference_file_states_same_values(self):
        for text in ["**35 kN**", "**145 kN**", "**110 kN**", "**9,3 N/mm (= 9,3 kN/m)",
                     "| **75%** |", "| **15%** |", "| **33%** |",
                     "| m | **1,20** | **1,00** | **0,85** | **0,65** |",
                     "| Cường độ I | **1,75** |", "| Sử dụng I | 1,00 |", "| Sử dụng III | 0,80 |",
                     "| Mỏi I | 1,50 |", "| Mỏi II | 0,75 |",
                     "| **1,25** | **0,90** |", "| **1,50** | **0,65** |",
                     "**L/800**", "**L/1000**", "**9 000 mm**"]:
            self.assertIn(text, REFERENCE, f"reference file no longer contains {text!r}")


class SimpleSpanHandCalcs(unittest.TestCase):
    L = 30.0

    def test_truck_moment_midspan(self):
        # middle axle at midspan, rear spacing 4.3 m:
        # 145*7.5 + 145*15*10.7/30 + 35*10.7*15/30 = 1087.5 + 775.75 + 187.25
        m, s = t.vehicle_moment(self.L, 15.0, t.truck_configs())
        self.assertAlmostEqual(m, 2050.5, places=6)
        self.assertAlmostEqual(s, 4.3, places=6)

    def test_truck_absolute_max_moment(self):
        # resultant theorem: 325/30*(15 - 1.455/2)^2 - 35*4.3 = 2056.3 kN·m
        r = t.hl93_simple_span(self.L)
        self.assertAlmostEqual(r["m_truck"], 2056.3, delta=0.5)

    def test_tandem_moment_midspan(self):
        m, _ = t.vehicle_moment(self.L, 15.0, t.tandem_configs())
        self.assertAlmostEqual(m, 110 * 7.5 + 110 * 15 * 13.8 / 30, places=6)   # 1584.0

    def test_lane_moment_and_shear(self):
        self.assertAlmostEqual(t.lane_moment(self.L, 15.0), 9.3 * 30 ** 2 / 8)
        self.assertAlmostEqual(t.lane_support_shear(self.L), 9.3 * 30 / 2)

    def test_truck_support_shear(self):
        # 145 at 0, 145 at 4.3, 35 at 8.6
        expected = 145 + 145 * 25.7 / 30 + 35 * 21.4 / 30
        v, s = t.vehicle_support_shear(self.L, t.truck_configs())
        self.assertAlmostEqual(v, expected, places=6)
        self.assertAlmostEqual(s, 4.3, places=6)

    def test_axles_off_span_ignored(self):
        # 5 m span: the truck cannot fit; only axles on the span count
        m, _ = t.vehicle_moment(5.0, 2.5, t.truck_configs())
        self.assertAlmostEqual(m, 145 * 2.5 / 2, places=6)

    def test_lane_deflection_midspan(self):
        EI = 2.5e7
        self.assertAlmostEqual(t.lane_deflection(self.L, EI, 15.0), 5 * 9.3 * 30 ** 4 / (384 * EI))

    def test_point_deflection_midspan(self):
        EI, P = 2.5e7, 100.0
        self.assertAlmostEqual(t._point_deflection(self.L, EI, 15.0, 15.0, P), P * 30 ** 3 / (48 * EI))
        # Maxwell reciprocity
        self.assertAlmostEqual(t._point_deflection(self.L, EI, 10.0, 22.0, P),
                               t._point_deflection(self.L, EI, 22.0, 10.0, P))


class Combinations(unittest.TestCase):
    def test_strength_i_example_from_skill(self):
        r = t.combine("str1", dc=420, dw=180, truck=250, lane=80)
        self.assertAlmostEqual(r["total"], 1516.875)

    def test_im_not_applied_to_lane(self):
        r = t.combine("ser1", dc=0, dw=0, truck=0, lane=100)
        self.assertAlmostEqual(r["total"], 100.0)

    def test_minimum_factors(self):
        r = t.combine("str1", dc=100, dw=100, truck=0, use_min=True)
        self.assertAlmostEqual(r["total"], 90 + 65)

    def test_fatigue_ignores_lane_dead_load_and_m(self):
        r = t.combine("fat1", dc=500, dw=200, truck=100, lane=80, m=1.2)
        self.assertAlmostEqual(r["total"], 1.5 * 100 * 1.15)

    def test_deck_joint_im(self):
        r = t.combine("str1", dc=0, dw=0, truck=100, deck_joint=True)
        self.assertAlmostEqual(r["total"], 1.75 * 175)


if __name__ == "__main__":
    unittest.main()
