"""Mechanical completeness and source-binding checks for the 1998 Shanghai arts draft."""
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = PROJECT / "1998_上海卷_文科"
QUESTIONS = PAPER / "题面转录草稿.md"
MANIFEST = PROJECT / "source-manifest.json"
SOURCE_ID = "src-8c86b3e592e594953609fe09d0c182d5252c944006503dfb10e8efa1962aeca7"
SOURCE_SHA256 = "c747bff56863a349aa9432b1616630a249cd7668ead997a5bbe1fefa2616f848"


class Shanghai1998ArtsTranscriptionTests(unittest.TestCase):
    def test_q12_preserves_printed_tg_notation(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        q12 = text.split("**12．**", 1)[1].split("**13．**", 1)[0]
        self.assertIn(r"（C）$y=\operatorname{tg}2x$", q12)
        self.assertNotIn(r"（C）$y=\tan2x$", q12)

    def test_q18_preserves_printed_multiplication_dot(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        q18 = text.split("**18．", 1)[1].split("**19．", 1)[0]
        self.assertIn(r"z_1\cdot z_2", q18)

    def test_question_numbers_are_contiguous_and_match_the_paper_total(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．", text, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertIn("全卷22题、满分150分", text)
        self.assertIn("填空题（1—11，每题4分，共44分）", text)
        self.assertIn("选择题（12—16，每题4分，共20分）", text)
        self.assertIn("解答题（17—22，共86分", text)

    def test_only_local_vector_sources_are_linked_for_the_three_figures(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        links = re.findall(r"\]\((figures/[^)]+\.tex)\)", text)
        self.assertEqual(len(links), 3)
        self.assertEqual(len(set(links)), 3)
        for link in links:
            self.assertTrue((PAPER / link).is_file(), link)
        self.assertNotRegex(text, r"!\[[^]]*\]\([^)]*\.(?:png|jpe?g)\)")

    def test_fixed_source_is_still_unbound_and_has_expected_fingerprint(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        matches = [record for record in manifest["sources"] if record["source_id"] == SOURCE_ID]
        self.assertEqual(len(matches), 1)
        source = matches[0]
        self.assertEqual(source["upstream_path"], "普通高考/1998/1998上海文.pdf")
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 6)
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        self.assertIsNone(source["paper_relation"])


if __name__ == "__main__":
    unittest.main()
