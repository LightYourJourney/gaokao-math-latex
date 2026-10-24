"""Completeness and fixed-source guards for the 1998 Shanghai science draft."""
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = PROJECT / "1998_上海卷_理科"
QUESTIONS = PAPER / "题面转录草稿.md"
MANIFEST = PROJECT / "source-manifest.json"
SOURCE_ID = "src-0965cb55b028616d561b059acccc3e23188f14aab4f25bd949c2c170a29d5d66"
SOURCE_SHA256 = "9abf8273c0bc577e5a8a6df9c72dd9ba5040ad11bb3d470918ce7bcf48168a0f"


class Shanghai1998ScienceTranscriptionTests(unittest.TestCase):
    def test_question_numbers_and_score_sections_are_complete(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．", text, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertIn("全卷22题、满分150分", text)
        self.assertIn("填空题（1—11，每题4分，共44分）", text)
        self.assertIn("选择题（12—16，每题4分，共20分）", text)
        self.assertIn("解答题（17—22，共86分", text)
        self.assertEqual(44 + 20 + 86, 150)

    def test_high_risk_formula_and_source_wording_anchors_are_present(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        self.assertIn(r"$\lg 20+\log_{100}25=$", text)
        self.assertNotIn(r"$\\lg", text)
        for anchor in (
            r"\sqrt a\cos x",
            r"\log_{100}25",
            r"\{|b_n|\}",
            r"\overline A\cup\overline B",
            r"(z-2)i=1+i",
            r"\frac{37\pi}{6}-2\alpha",
            r"\operatorname{tg}2x",
            r"y^2=\frac12(x-2)",
            r"4B_n-12A_n=13n",
            r"-265<c_{10}<-125",
        ):
            self.assertIn(anchor, text)
        self.assertIn("](figures/1998_shanghai_science_q19_prism.tex)", text)
        self.assertIn("4B_n-12A_n=13n\n\\]。", text)
        self.assertNotIn("4B_n-12A_n=13n。", text)
        self.assertNotRegex(text, r"!\[[^]]*\]\([^)]*\.(?:png|jpe?g)\)")

    def test_fixed_source_is_ready_unbound_and_matches_recorded_fingerprint(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        matches = [record for record in manifest["sources"] if record["source_id"] == SOURCE_ID]
        self.assertEqual(len(matches), 1)
        source = matches[0]
        self.assertEqual(source["upstream_path"], "普通高考/1998/1998上海理.pdf")
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 6)
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["paper_id"], "gk-1998-regular-shanghai-science")
        self.assertEqual(source["paper_relation"], "canonical")


if __name__ == "__main__":
    unittest.main()
