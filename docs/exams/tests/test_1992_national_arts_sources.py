"""Arts source intake and bounded reuse, without accepting source typos."""
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1992_全国卷_文科"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class NationalArts1992SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (PROJECT / "题面转录草稿.md").read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.text)
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))

    def test_fixed_source_identity_and_draft_hash(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(s for s in manifest["sources"] if s["source_id"] == self.record["source_id"])
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["upstream_path"], self.record["upstream_path"])
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["paper_id"], "gk-1992-regular-national-arts")
        self.assertEqual(source["paper_relation"], "canonical")
        mirror = self.record["archive_mirror_verification"]
        self.assertEqual(mirror["repository"], "deekur/gaokaomath")
        self.assertEqual(mirror["commit"], "34c13a6cf632c0b69c95f89b9b923bbc4a08924d")
        self.assertEqual(mirror["contents_api_path"].split("/contents/", 1)[1], self.record["upstream_path"])
        self.assertEqual(mirror["git_blob_oid"], source["git_blob_oid"])
        self.assertEqual(mirror["sha256"], source["artifact"]["sha256"])
        self.assertEqual(mirror["page_count"], source["artifact"]["page_count"])
        self.assertEqual(mirror["result"], "exact-bytes-match-manifest")
        self.assertIn("出版者", mirror["limitation"])
        self.assertEqual(self.record["source_authenticity"], "fixed-upstream-typeset-copy-unverified-publisher")
        self.assertEqual(hashlib.sha256((PROJECT / "题面转录草稿.md").read_bytes()).hexdigest(), self.record["draft_sha256"])

    def test_28_questions_with_subparts_only_at_arts_q28(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 29)))
        self.assertEqual({q.number: q.subparts for q in self.questions if q.subparts}, {28: (1, 2)})
        self.assertEqual(self.record["page_map"][0]["printed_page"], "43")
        self.assertEqual(len(self.record["page_map"][0]["columns"]), 3)

    def test_all_18_choices_and_math_delimiters(self):
        for q in self.questions[:18]:
            for letter in "ABCD":
                self.assertEqual(q.body.count("（" + letter + "）"), 1)
        self.assertEqual(self.text.count("$") % 2, 0)
        self.assertEqual(self.text.count(r"\begin{cases}"), self.text.count(r"\end{cases}"))

    def test_source_contradictions_remain_visible_without_guessing_x_or_minus(self):
        self.assertIn(r"\dfrac{e^x-e^x}{2}", self.questions[15].body.split("\n\n")[0])
        stem = self.questions[26].body.split("\n\n")[0]
        self.assertIn("$2-2y+1=0$", stem)
        self.assertNotIn("x-2y+1", stem)
        self.assertNotIn("2x-2y+1", stem)
        self.assertEqual([i["question_number"] for i in self.record["source_issues"]], [16, 27])
        self.assertTrue(all(i["status"] == "needs-review" for i in self.record["source_issues"]))

    def test_17_reused_stems_preserve_verified_number_mapping_not_receipts(self):
        reused = self.record["reused_transcription"]
        file = (PROJECT / reused["source_path"]).resolve()
        self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), reused["source_sha256"])
        science = {q.number: q for q in solution_sources.parse_question_blocks(file.read_text(encoding="utf-8"))}
        mapping = {int(k): v for k, v in reused["arts_to_science"].items()}
        self.assertEqual(len(mapping), 17)
        self.assertEqual(mapping[3], 2)
        self.assertEqual(mapping[28], 27)
        def without_editorial(body):
            lines = [line for line in body.splitlines() if not line.startswith((">", "[第"))]
            return re.sub(r"\s+", "", "\n".join(lines))
        for arts_number, science_number in mapping.items():
            arts_body = self.questions[arts_number - 1].body
            if arts_number == 18:
                self.assertTrue(arts_body.startswith("已知长方体"))
                arts_body = arts_body.removeprefix("已知")
            self.assertEqual(without_editorial(arts_body), without_editorial(science[science_number].body))

    def test_distinct_questions_keep_their_own_conditions(self):
        self.assertIn(r"\dfrac{x^2}{25}+\dfrac{y^2}{16}=1", self.questions[1].body)
        self.assertIn(r"\left(\dfrac x2-\dfrac1{\sqrt[3]x}\right)^8", self.questions[3].body)
        self.assertIn("8x+6y=25", self.questions[7].body)
        self.assertIn(r"\tan\alpha<\cot\beta", self.questions[12].body)
        self.assertIn(r"z-2|z|=-7+4i", self.questions[24].body)
        self.assertIn(r"AA_1", self.questions[25].body)
        self.assertIn(r"CC_1", self.questions[25].body)

    def test_missing_scores_answers_and_unfinished_figures_are_not_claimed(self):
        for field in ("official_answer", "question_scores", "total_score", "paper_id"):
            self.assertIsNone(self.record[field])
        self.assertFalse(self.record["source_has_answers"])
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["mathematical_verification_status"], "independently-reviewed")
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertEqual([q.number for q in self.questions if "题图待重绘" in q.body], [])
        self.assertEqual(self.record["question_figures_pending"], [])

    def test_three_vector_sources_and_controlled_reuse_without_raster(self):
        figures = self.record["figure_files"]
        self.assertEqual([f["question_number"] for f in figures], [6, 14, 26])
        for f in figures:
            file = PROJECT / f["path"]
            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), f["sha256"])
            target = "../math-gaokao-latex/1992_全国卷_文科/" + f["path"]
            self.assertEqual((ROOT.parent / "1992" / target).resolve(), file.resolve())
            self.assertEqual(self.questions[f["question_number"] - 1].body.count(f"]({target})"), 1)
            text = file.read_text(encoding="utf-8")
            self.assertEqual(text.count(r"\begin{tikzpicture}"), 1)
            self.assertEqual(text.count(r"\end{tikzpicture}"), 1)
            for command in (r"\includegraphics", r"\input", r"\write18", r"\documentclass"):
                self.assertNotIn(command, text)
            if "reused_from" in f:
                source = (PROJECT / f["reused_from"]).resolve()
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), f["reused_sha256"])
                without_comments = lambda t: "\n".join(line for line in t.splitlines() if not line.lstrip().startswith("%"))
                self.assertEqual(without_comments(text), without_comments(source.read_text(encoding="utf-8")))

    def test_native_text_candidate_and_incremental_cache_are_not_fidelity_gates(self):
        analysis = self.record["text_analysis"]
        self.assertEqual(analysis["classification"], "text_layer_candidate")
        self.assertTrue(analysis["requires_content_review"])
        self.assertEqual(analysis["ocr_calls"], 0)
        self.assertEqual(analysis["resume_check"]["hits"], 1)
        self.assertEqual(analysis["resume_check"]["misses"], 0)
        for name in (analysis["cache_path"], self.record["render"]["path"]):
            path = Path(name)
            self.assertFalse(path.is_absolute())
            self.assertNotIn("..", path.parts)
            self.assertEqual(path.parts[0], ".work")


if __name__ == "__main__":
    unittest.main()
