"""Q5: the plotted intervals and labels must represent [-4,-2) union (3,4]."""

import json
import re
import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
sys.path.insert(0, str(ROOT.parent / "math-gaokao-2017-2026/tools"))
import md2tex

NAME = "f1977_t5_numberline"
FIGURE = ROOT / "1977_上海卷_理科/figures" / (NAME + ".tex")
SOURCE = REPO / "1977/1977_数学真题_上海理_解析正文.md"
TARGET = "../math-gaokao-latex/1977_上海卷_理科/figures/" + NAME + ".tex"


class ShanghaiScience1977NumberLineTests(unittest.TestCase):
    def figure(self):
        self.assertTrue(FIGURE.is_file(), "ASCII spacing is not a positioned number line")
        return FIGURE.read_text(encoding="utf-8")

    def test_drawn_intervals_match_both_inequalities_including_boundaries(self):
        text = self.figure()
        closed = {Fraction(x) for x in re.findall(r"\\fill\s*\(([-\d.]+),0\)\s*circle", text)}
        opened = {Fraction(x) for x in re.findall(r"\\draw\[fill=white,thick\]\s*\(([-\d.]+),0\)\s*circle", text)}
        self.assertEqual(closed, {-4, 4})
        self.assertEqual(opened, {-2, 3})
        selected = re.findall(r"\\draw\[very thick\]\s*(.*?);", text)
        segments = [(Fraction(a), Fraction(b)) for line in selected for a, b in re.findall(r"\(([-\d.]+),0\)--\(([-\d.]+),0\)", line)]
        self.assertEqual(segments, [(Fraction(-4), Fraction(-2)), (Fraction(3), Fraction(4))])
        for x in (Fraction(n, 4) for n in range(-24, 25)):
            with self.subTest(x=x):
                plotted = x in closed or any(a < x < b for a, b in segments)
                self.assertEqual(plotted, 16 - x*x >= 0 and x*x - x - 6 > 0)

    def test_numeric_labels_share_endpoint_coordinates(self):
        labels = re.findall(r"\\node\[below=5pt\] at \(([-\d.]+),0\) \{\$([-\d.]+)\$\}", self.figure())
        self.assertEqual([(Fraction(x), Fraction(label)) for x, label in labels], [(-4, -4), (-2, -2), (3, 3), (4, 4)])

    def test_canonical_question_5_uses_registered_vector_link(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        paper = next(p for p in manifest["papers"] if p["paper_id"] == "gk-1977-regular-shanghai-science")
        registered = next((f for f in paper["figure_files"] if f["path"].endswith(NAME + ".tex")), None)
        self.assertIsNotNone(registered, "number-line input must be registered, not a dangling link")
        self.assertEqual(registered["expected_occurrences"], 1)
        body = SOURCE.read_text(encoding="utf-8").split("### 第 5 题\n", 1)[1].split("### 第 6 题\n", 1)[0]
        result = md2tex.convert_markdown(body, md2tex.ConversionContext(figure_map={TARGET: NAME}))
        self.assertEqual(result.referenced_figures, (NAME,))
        self.assertIn(r"\input{figures/" + NAME + "}", result.text)
        self.assertNotIn("~~~", result.text)
        self.assertIn(r"[-4,-2)\cup(3,4]", result.text)


if __name__ == "__main__":
    unittest.main()
