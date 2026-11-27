"""Kiểm tra SKILL.md định tuyến tới đủ file tham chiếu và giữ frontmatter trong giới hạn.

Run:  python3 -m unittest discover -s skills/thiet-ke-cau-11823/scripts
"""
from __future__ import annotations

import pathlib
import re
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
REFERENCE_DIR = SKILL_DIR / "references"
SKILL_MD = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")


def referenced_files(skill_md: str) -> set[str]:
    """Mọi `references/<ten>.md` được nhắc tới trong SKILL.md."""
    return set(re.findall(r"references/[\w.-]+\.md", skill_md))


class SkillRouting(unittest.TestCase):
    def test_every_reference_file_is_routed(self):
        on_disk = {f"references/{p.name}" for p in REFERENCE_DIR.glob("*.md")}
        self.assertEqual(on_disk, referenced_files(SKILL_MD))

    def test_routed_files_exist(self):
        for f in referenced_files(SKILL_MD):
            self.assertTrue((SKILL_DIR / f).is_file(), f)

    def test_frontmatter(self):
        fm = SKILL_MD.split("---")[1]
        self.assertRegex(fm, r"(?m)^name: thiet-ke-cau-11823$")
        desc = re.search(r"(?m)^description: (.*)$", fm).group(1)
        self.assertLessEqual(len(desc), 1024)


class Part4Reference(unittest.TestCase):
    TEXT = (REFERENCE_DIR / "phan-4-phan-bo.md").read_text(encoding="utf-8")

    def test_all_tables_present_with_page(self):
        for t, page in [(4, 40), (5, 42), (6, 44), (7, 46), (8, 48), (9, 49),
                        (10, 50), (11, 51), (12, 53), (13, 54)]:
            self.assertRegex(self.TEXT, rf"Bảng {t}\b.*tr\.\s*{page}")

    def test_clauses(self):
        for c in ["6.2.2.1", "6.2.2.2.1", "6.2.2.2.2", "6.2.2.2.3", "6.2.2.2.4",
                  "6.2.2.2.5", "6.2.2.3.1", "6.2.2.3.2", "6.2.2.3.3", "6.2.3"]:
            self.assertIn(c, self.TEXT)


if __name__ == "__main__":
    unittest.main()
