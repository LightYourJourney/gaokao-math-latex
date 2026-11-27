"""Source and completeness guards for the 1999 Shanghai science draft."""
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = PROJECT / "1999_上海卷_理科"
QUESTIONS = PAPER / "题面转录草稿.md"
FIGURE_LIST = PAPER / "图表清单.md"
SOURCE_RECORD = PAPER / "来源校对.json"
MANIFEST = PROJECT / "source-manifest.json"
SOURCE_ID = "src-f25a93d31d085187de864aff4bec94d037a9f96cb3cfc6682b87adfee4bfe97d"
SOURCE_SHA256 = "055fd4d4468dd6db86a49b8addc9209ab497987269aea96a72f0b26ad35cd9dc"


class Shanghai1999ScienceTranscriptionTests(unittest.TestCase):
    def test_question_numbers_sections_and_score_total(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．", text, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertIn("填空题（1—12，每题4分，共48分）", text)
        self.assertIn("选择题（13—16，每题4分，共16分）", text)
        self.assertIn("解答题（17—22，共86分", text)
        self.assertEqual(48 + 16 + 86, 150)

    def test_source_wording_and_high_risk_math_are_transcribed(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        for anchor in (
            r"\operatorname{tg}\left(\arccos\frac{\sqrt2}{2}-\frac\pi6\right)",
            r"\log_2 x+1\quad (x\ge4)",
            r"\left(x^3+\frac2{x^2}\right)^5",
            r"\vec a=\{2,1\}",
            r"5\rho^2\cos2\theta+\rho^2-24=0",
            r"(x-2)^2+y^2=3",
            r"\frac{2x-1}{x+2}<1",
            r"x^2+(4+i)x+4+ai=0",
            r"\bar z(1-ci)",
            r"a_2=4",
            r"a_4=16",
            r"\min\{g(a),S(a)\}",
            r"\frac{x^2}{a^2}+\frac{y^2}{b^2}=1",
            r"y=\frac1x",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, text, msg=anchor)
        self.assertIn("底面 $ABCD$ 是一直角梯形", text)
        self.assertIn("沟宽$AB$为2米", text)
        self.assertIn("1999 年第 4 期", text)
        self.assertNotRegex(text, r"!\[[^]]*\]\([^)]*\.(?:png|jpe?g)\)")

    def test_q20_q21_source_text_rechecks_do_not_promote_paper_review(self):
        record = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))
        rechecks = record.get("source_text_rechecks", [])
        self.assertEqual([item["question_number"] for item in rechecks], [20, 21])
        for item in rechecks:
            with self.subTest(question=item["question_number"]):
                self.assertEqual(item["pdf_page"], 2)
                self.assertEqual(item["printed_page"], "4-36")
                self.assertEqual(item["result"], "transcription-matches-fixed-scan")
                self.assertEqual(item["review_status"], "pending-independent-review")
        self.assertEqual(record["transcription_status"], "transcribed-reviewed")
        self.assertEqual(record["review_status"], "reviewed")

    def test_question_figures_link_to_vector_sources_not_embedded_rasters(self):
        text = QUESTIONS.read_text(encoding="utf-8")
        figure_list = FIGURE_LIST.read_text(encoding="utf-8")
        source_record = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))
        for name in ("1999_shanghai_science_q20_pyramid.tex", "1999_shanghai_science_q21_canal.tex"):
            with self.subTest(figure=name):
                self.assertIn(f"](figures/{name})", text)
                self.assertIn(name, figure_list)
        self.assertEqual(
            [figure["status"] for figure in source_record["figures"]],
            [
                "vector-draft-rendered-independent-topology-review-passed",
                "vector-draft-rendered-pending-independent-review",
            ],
        )
        self.assertNotIn("待矢量重绘", text)
        self.assertNotRegex(text, r"!\[[^]]*\]\([^)]*\.(?:png|jpe?g)\)")

    def test_fixed_source_fingerprint_and_unverified_boundary(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        matches = [source for source in manifest["sources"] if source["source_id"] == SOURCE_ID]
        self.assertEqual(len(matches), 1)
        source = matches[0]
        self.assertEqual(source["upstream_path"], "普通高考/1999/1999上海理.pdf")
        self.assertEqual(source["git_blob_oid"], "1d76d728820d9302c707ccdfddddd9ec430df2b3")
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 5)
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["paper_id"], "gk-1999-regular-shanghai-science")
        self.assertEqual(source["paper_relation"], "canonical")

        record = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))
        self.assertEqual(record["source"]["source_id"], SOURCE_ID)
        self.assertEqual(record["source"]["sha256"], SOURCE_SHA256)
        self.assertEqual(record["source"]["page_count"], 5)
        self.assertEqual(record["paper_id"], "gk-1999-regular-shanghai-science")
        self.assertEqual(record["source_authenticity"], "unverified")
        self.assertIsNone(record["official_answer"])
        self.assertEqual(record["review_status"], "reviewed")


if __name__ == "__main__":
    unittest.main()
