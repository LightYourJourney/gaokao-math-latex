"""1997 全国理科解析版分页回归。"""

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent.parent.parent
PAPER_ID = "gk-1997-regular-national-science"
sys.path.insert(0, str(ROOT / "tools"))

import generate_projects


class NationalScience1997LayoutTests(unittest.TestCase):
    def test_q23_part2_keeps_conjunction_with_its_dot_product(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        paper = next(item for item in manifest["papers"] if item["paper_id"] == PAPER_ID)
        sources = generate_projects.paper_sources(paper)
        result = generate_projects.generate_project(REPOSITORY_ROOT, sources)
        target = "math-gaokao-latex/%s/answers.tex" % sources.project_dir
        answers_tex = result.targets[target].decode("utf-8")
        question_23 = answers_tex.split(r"\gksolhead{23}{", 1)[1].split(
            r"\end{answer}", 1
        )[0]

        self.assertIn(
            r"且 $\overrightarrow{AE}\cdot\overrightarrow{D_1F}=2-2=0$",
            question_23,
        )


if __name__ == "__main__":
    unittest.main()
