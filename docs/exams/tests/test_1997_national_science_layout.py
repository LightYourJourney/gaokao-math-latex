"""1997 全国理科解析版分页回归。"""

import json
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parent
PAPER_ID = "gk-1997-regular-national-science"
sys.path.insert(0, str(ROOT / "tools"))

import generate_projects


class NationalScience1997LayoutTests(unittest.TestCase):
    def test_q3_origin_labels_are_clear_of_curves_and_tick_labels(self):
        figure = (ROOT / "1997_全国卷_理科/figures/f1997_t3_graphs.tex").read_text(
            encoding="utf-8"
        )
        panels = re.split(r"^  % \(([A-D])\)$", figure, flags=re.MULTILINE)
        panel_sources = dict(zip(panels[1::2], panels[2::2]))
        expected_positions = {
            "A": "above left",
            "B": "above right",
            "C": "above left",
            "D": "above left",
        }

        for option, position in expected_positions.items():
            with self.subTest(option=option):
                match = re.search(
                    r"\\node\[(?P<options>[^]]+)\] at \(axis cs:0,0\) \{\$O\$\};",
                    panel_sources[option],
                )
                self.assertIsNotNone(match)
                self.assertTrue(match["options"].startswith(position))
                if option == "B":
                    self.assertIn("xshift=-2pt", match["options"])

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
