import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1991_上海卷"
ANSWER_FILE = ROOT.parent / "1991/1991_数学真题_上海_答案要点.md"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class Shanghai1991SourceIntakeTests(unittest.TestCase):
    """Source-intake checks; these do not certify mathematical correctness."""

    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))
        cls.question_text = (PROJECT / "题面转录草稿.md").read_text(encoding="utf-8")
        cls.answer_text = ANSWER_FILE.read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.question_text)
        cls.answers = solution_sources.parse_answer_points(cls.answer_text)

    def test_source_identity_matches_manifest_and_saved_content_hashes(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(s for s in manifest["sources"] if s["source_id"] == self.record["source_id"])
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["upstream_path"], self.record["upstream_path"])
        for file, key in (
            (PROJECT / "题面转录草稿.md", "draft_sha256"),
            (ANSWER_FILE, "answer_source_sha256"),
        ):
            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), self.record[key])

    def test_all_27_question_and_answer_slots_and_subparts_align(self):
        expected = list(range(1, 28))
        self.assertEqual([q.number for q in self.questions], expected)
        self.assertEqual([a.number for a in self.answers], expected)
        self.assertEqual([q.subparts for q in self.questions], [a.subparts for a in self.answers])
        self.assertEqual(
            {q.number: q.subparts for q in self.questions if q.subparts},
            {24: (1, 2, 3), 25: (1, 2), 27: (1, 2, 3)},
        )
        self.assertEqual(sum(self.record["question_scores"]), 150)
        self.assertEqual(len(self.record["question_scores"]), 27)
        for number, scores in self.record["subpart_scores"].items():
            self.assertEqual(sum(scores), self.record["question_scores"][int(number) - 1])

    def test_unread_exponents_and_unverified_status_cannot_be_hidden(self):
        unresolved = [q.number for q in self.questions if "待核指数" in q.body or "待核负分数指数" in q.body]
        self.assertEqual(unresolved, [8, 14, 20])
        self.assertEqual([r["question_number"] for r in self.record["unresolved_regions"]], unresolved)
        self.assertEqual(
            [q.number for q in self.questions if "题图待重绘" in q.body],
            self.record["question_figures_pending"],
        )
        self.assertEqual(self.record["question_figures_pending"], [])
        self.assertIsNone(self.record["paper_id"])
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertIn("不称“官方答案”", self.answer_text)
        for region in self.record["unresolved_regions"]:
            x0, y0, x1, y1 = region["bbox_pt"]
            self.assertTrue(0 <= x0 < x1 <= 519.29)
            self.assertTrue(0 <= y0 < y1 <= 724.52)

    def test_source_options_and_key_are_preserved_without_answer_backfill(self):
        for question in self.questions:
            if 11 <= question.number <= 20 and question.number != 14:
                for letter in "ABCD":
                    self.assertEqual(question.body.count("（" + letter + "）"), 1)
        self.assertEqual([a.answer_for(None) for a in self.answers[10:20]], list("BCBCBADADA"))
        self.assertIn(r"A\cap\overline B", self.questions[10].body)
        self.assertIn(r"\dfrac{32}{72}", self.questions[12].body)
        self.assertIn(r"2+\sqrt3", self.answers[21].answer_for(None))
        self.assertIn("或", self.answers[21].answer_for(None))

    def test_source_pages_cache_locators_and_math_delimiters(self):
        self.assertEqual([p["page"] for p in self.record["page_map"]], list(range(1, 8)))
        self.assertIsNone(self.record["page_map"][-1]["printed_page"])
        cached = self.record["ocr_cache"]["pages"]
        self.assertEqual([p["page"] for p in cached], list(range(1, 8)))
        for page in cached:
            for kind in ("render", "result"):
                path = Path(page[kind])
                self.assertFalse(path.is_absolute())
                self.assertNotIn("..", path.parts)
                self.assertEqual(path.parts[:2], (".work", "ocr-page-cache"))
        for text in (self.question_text, self.answer_text):
            self.assertEqual(text.count("$") % 2, 0)
            self.assertEqual(text.count(r"\begin{cases}"), text.count(r"\end{cases}"))

    def test_source_recheck_preserves_unresolved_scope_and_crop_identity(self):
        recheck = self.record["source_recheck"]
        self.assertEqual(recheck["status"], "unresolved")
        self.assertEqual(recheck["ocr_calls"], 0)
        self.assertEqual([c["question_number"] for c in recheck["crops"]], [8, 14, 20])
        for crop, original in zip(recheck["crops"], self.record["unresolved_regions"]):
            self.assertEqual(crop["page"], original["page"])
            self.assertEqual(crop["bbox_pt"], original["bbox_pt"])
            self.assertEqual(crop["dpi"], 600)
            self.assertTrue(crop["path"].startswith("/tmp/gk1991-shanghai-intake."))
            self.assertRegex(crop["sha256"], r"^[0-9a-f]{64}$")
        self.assertIn("已重绘并完成单页校样", self.question_text)
        self.assertNotIn("四处题图尚待TikZ重绘", self.question_text)

    def test_four_vector_sources_exist_without_raster_or_external_dependencies(self):
        figures = self.record["figure_files"]
        self.assertEqual([f["question_number"] for f in figures], [14, 24, 26, 27])
        for number, name in (
            (14, "choices"), (24, "tetrahedron"),
            (26, "parabola"), (27, "triangle"),
        ):
            file = PROJECT / "figures" / f"f1991_shanghai_q{number}_{name}.tex"
            self.assertTrue(file.is_file(), str(file))
            figure = next(f for f in figures if f["question_number"] == number)
            self.assertEqual(figure["path"], file.relative_to(PROJECT).as_posix())
            self.assertEqual(figure["sha256"], hashlib.sha256(file.read_bytes()).hexdigest())
            self.assertEqual(figure["source_page"], {14: 1, 24: 2, 26: 3, 27: 3}[number])
            self.assertEqual(figure["classification"],
                             "mathematical-reconstruction" if number == 26 else "source-faithful")
            # Draft links already use the canonical question file's relative base.
            target = "../math-gaokao-latex/1991_上海卷/" + figure["path"]
            self.assertEqual(self.questions[number - 1].body.count(f"]({target})"), 1)
            self.assertEqual((ANSWER_FILE.parent / target).resolve(), file.resolve())
            text = file.read_text(encoding="utf-8")
            self.assertEqual(text.count(r"\begin{tikzpicture}"), 1)
            self.assertEqual(text.count(r"\end{tikzpicture}"), 1)
            for command in (r"\includegraphics", r"\input", r"\write18", r"\documentclass"):
                self.assertNotIn(command, text)

    def test_q26_drawing_configuration_satisfies_only_the_given_conditions(self):
        # A compatible example for drawing, not additional coordinates in the stem.
        b = (Fraction(1, 2), Fraction(9, 4))
        c = (Fraction(-2), Fraction(6))
        p = (Fraction(-2, 11), Fraction(36, 11))
        q = (Fraction(20, 33), Fraction(12, 11))
        for x, y in (b, c):
            self.assertEqual(y, x * x + 2)
            self.assertEqual(y, -Fraction(3, 2) * (x - 2))
        self.assertTrue(c[0] < p[0] < b[0])
        self.assertEqual((b[0] - p[0]) / (p[0] - c[0]), b[1] / c[1])
        self.assertEqual(p[1], -Fraction(3, 2) * (p[0] - 2))
        self.assertEqual(q, ((p[0] + 2) / 3, p[1] / 3))

    def test_solution_figure_links_hashes_and_explanatory_classification(self):
        solution = (PROJECT / "复算草稿.md").read_text(encoding="utf-8")
        blocks = {q.number: q.body for q in solution_sources.parse_question_blocks(solution)}
        figures = self.record["solution_figure_files"]
        self.assertEqual([f["question_number"] for f in figures], [22, 24, 25])
        for figure in figures:
            file = PROJECT / figure["path"]
            self.assertEqual(figure["classification"], "explanatory-mathematical-reconstruction")
            self.assertEqual(figure["review_status"], "smoke-reviewed-main-session")
            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), figure["sha256"])
            target = "../math-gaokao-latex/1991_上海卷/" + figure["path"]
            self.assertEqual((ANSWER_FILE.parent / target).resolve(), file.resolve())
            self.assertEqual(blocks[figure["question_number"]].count(f"]({target})"), 1)
            text = file.read_text(encoding="utf-8")
            self.assertEqual(text.count(r"\begin{tikzpicture}"), 1)
            self.assertEqual(text.count(r"\end{tikzpicture}"), 1)
            for command in (r"\includegraphics", r"\input", r"\write18", r"\documentclass"):
                self.assertNotIn(command, text)
        self.assertIn("不冒称逐线复制", solution)
        self.assertIn("实点0保留、空心点$2i$排除", solution)


if __name__ == "__main__":
    unittest.main()
