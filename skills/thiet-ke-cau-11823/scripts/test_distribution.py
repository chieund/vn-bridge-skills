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


if __name__ == "__main__":
    unittest.main()
