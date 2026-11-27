"""Checks that SKILL.md routes to every reference file and stays within frontmatter limits.

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
    """Every `references/<name>.md` mentioned in SKILL.md."""
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


if __name__ == "__main__":
    unittest.main()
