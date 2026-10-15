"""Source-bound completeness checks for the 1994 Shanghai mathematics paper."""
import hashlib
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PAPER_ID = "gk-1994-shanghai"
PROJECT_DIR = ROOT / "1994_上海卷"
QUESTION_SOURCE = REPO / "1994/1994_数学真题_上海_试题.md"
ANSWER_SOURCE = REPO / "1994/1994_数学真题_上海_答案要点.md"
SOLUTION_SOURCE = REPO / "1994/1994_数学真题_上海_解析正文.md"
COMBINED_SOURCE = REPO / "1994/1994_数学真题_上海_含解析.md"
RECORD = PROJECT_DIR / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"
SOURCE_ID = "src-175369213dde711e3bba990974dca1216e7e4ef6ed65cbc9e197dc39d81eba65"


class Shanghai1994SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next(
            (s for s in cls.manifest["sources"] if s["source_id"] == SOURCE_ID), None
        )
        cls.paper = next(
            (p for p in cls.manifest["papers"] if p["paper_id"] == PAPER_ID), None
        )
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.questions = QUESTION_SOURCE.read_text(encoding="utf-8") if QUESTION_SOURCE.is_file() else ""
        cls.answers = ANSWER_SOURCE.read_text(encoding="utf-8") if ANSWER_SOURCE.is_file() else ""
        cls.solutions = SOLUTION_SOURCE.read_text(encoding="utf-8") if SOLUTION_SOURCE.is_file() else ""
        cls.combined = COMBINED_SOURCE.read_text(encoding="utf-8") if COMBINED_SOURCE.is_file() else ""

    def test_canonical_paper_is_bound_to_the_fixed_scan(self):
        self.assertIsNotNone(self.source)
        self.assertIsNotNone(self.paper)
        self.assertEqual(self.source["source_state"], "ready")
        self.assertEqual(self.source["upstream_path"], "普通高考/1994/1994上海.pdf")
        self.assertEqual(self.source["git_blob_oid"], "a5b42d8e3935f34a2d9eeee96f1a3dc66f941663")
        self.assertEqual(self.source["artifact"]["sha256"], "2321a1438961a48e8951b83cdb4b71e4afa127e1981420a6ba7d1a9e1eddc22d")
        self.assertEqual(self.paper["source_ids"], [SOURCE_ID])
        self.assertEqual(self.paper["question_count"], 26)
        self.assertEqual(self.paper["production_state"], "blocked")
        self.assertEqual(self.paper["issue_ids"], self.record["issue_ids"])
        self.assertEqual(self.record["pdf_sha256"], self.source["artifact"]["sha256"])
        self.assertEqual(self.record["question_source_sha256"], hashlib.sha256(QUESTION_SOURCE.read_bytes()).hexdigest())
        self.assertEqual(self.record["answer_source"]["sha256"], hashlib.sha256(ANSWER_SOURCE.read_bytes()).hexdigest())
        self.assertEqual(self.record["solution_source"]["sha256"], hashlib.sha256(SOLUTION_SOURCE.read_bytes()).hexdigest())
        self.assertEqual(self.record["combined_rendered_sha256"], hashlib.sha256(COMBINED_SOURCE.read_bytes()).hexdigest())

    def test_all_questions_and_printed_page_spans_are_accounted_for(self):
        self.assertTrue(QUESTION_SOURCE.is_file(), "canonical question transcription is missing")
        if not self.record:
            self.fail("source audit record is missing")
            return
        headings = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.questions, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 27)))
        self.assertEqual(self.record["question_count"], 26)
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "fill-in", "first": 1, "last": 10},
            {"type": "single-choice", "first": 11, "last": 20},
            {"type": "solution", "first": 21, "last": 26},
        ])
        by_number = {item["question_number"]: item["source_pages"] for item in self.record["question_sources"]}
        self.assertEqual(by_number[15], [1, 2])
        self.assertEqual(by_number[21], [2, 3])
        self.assertTrue(all(by_number[number] == [1] for number in range(1, 15)))
        self.assertTrue(all(by_number[number] == [2] for number in range(16, 21)))
        self.assertTrue(all(by_number[number] == [2] for number in range(22, 26)))
        self.assertEqual(by_number[26], [3])

    def test_source_specific_formulas_and_conditions_are_preserved(self):
        required = (
            r"|x+1|<1",
            r"\sin\left(\dfrac12\arccos\dfrac18\right)",
            r"\log_3(x-1)=\log_9(x+5)",
            r"\dfrac{y^2}{2}-x^2=1",
            r"\rho=-\dfrac1{\cos\theta}",
            r"\dfrac{3\pi}4",
            r"\frac{|OP|}{|OQ|}=t\sqrt{t^2-1}",
            r"a_n a_{n+1}+a_{n+1}a_{n+2}>a_{n+2}a_{n+3}",
            r"(0,+\infty)",
        )
        normalized_questions = re.sub(r"\s+", "", self.questions)
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(re.sub(r"\s+", "", fragment), normalized_questions)

    def test_cjk_sentence_stops_in_generated_math_use_text_font(self):
        math_spans = re.compile(
            r"\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)|"
            r"(?<!\\)\$(?!\$)(?:\\.|[^$])*?(?<!\\)\$(?!\$)",
            re.DOTALL,
        )
        sources = (PROJECT_DIR / "questions.tex", PROJECT_DIR / "answers.tex")
        offenders = []
        for path in sources:
            text = path.read_text(encoding="utf-8")
            for span in math_spans.finditer(text):
                unwrapped = span.group().replace(r"\text{。}", "")
                for punctuation in re.finditer("。", unwrapped):
                    offset = span.start() + punctuation.start()
                    line = text.count("\n", 0, offset) + 1
                    offenders.append(f"{path.relative_to(REPO)}:{line}")
        self.assertEqual(offenders, [], "数学字体中有未包装的句号: " + ", ".join(offenders))

    def test_printed_answers_are_attributed_and_q25_source_discrepancy_is_retained(self):
        self.assertTrue(ANSWER_SOURCE.is_file(), "canonical answer transcription is missing")
        if not self.record:
            self.fail("source audit record is missing")
            return
        self.assertIn("来源印载", self.answers)
        self.assertIn("official_answer", self.record)
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertIn(r"t\ge2", self.answers)
        self.assertIn("原印载条件与上下文不一致", self.answers)
        self.assertIn("Q25", self.answers)
        self.assertEqual(self.record["review_status"], "needs-review")

    def test_q25_coordinate_derivation_remains_provisional_not_official(self):
        checks = self.record.get("derived_solution_checks", [])
        self.assertEqual(len(checks), 1)
        check = checks[0]
        self.assertEqual(check["question_id"], "src-175369213dde711e3bba990974dca1216e7e4ef6ed65cbc9e197dc39d81eba65:q025")
        self.assertEqual(check["status"], "derived-pending-independent-review")
        self.assertFalse(check["independent_review"])
        self.assertIsNone(check["official_answer"])
        self.assertEqual(check["jacobian"], "2(1+t^2)")
        self.assertEqual(check["piecewise_area"], "2(1-t+t^2-t^3) for 0<t<=1/2; (t+1/t)/2 for t>=1/2")
        self.assertEqual(check.get("first_branch_derivative"), "2(-1+2t-3t^2)<0 (discriminant -8)")
        self.assertEqual(check["monotonicity"], "decreasing on (0,1]; increasing on [1,+infinity)")
        self.assertIn("打印答案的第二支 t>=2", check["source_conflict"])

    def test_each_source_diagram_is_registered_vector_latex(self):
        self.assertTrue(RECORD.is_file(), "source audit record is missing")
        figures = self.record.get("figure_files", [])
        self.assertEqual({item["question_number"] for item in figures}, {11, 23, 25})
        for item in figures:
            path = PROJECT_DIR / item["path"]
            self.assertEqual(path.suffix, ".tex")
            self.assertTrue(path.is_file(), item["path"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])
            markdown_target = Path(os.path.relpath(path, QUESTION_SOURCE.parent)).as_posix()
            self.assertIn(f"]({markdown_target})", self.questions + self.solutions)
        raster_suffixes = {".png", ".jpg", ".jpeg"}
        tracked_candidates = [p for p in PROJECT_DIR.rglob("*") if p.is_file() and ".work" not in p.parts]
        self.assertFalse([p for p in tracked_candidates if p.suffix.lower() in raster_suffixes])


if __name__ == "__main__":
    unittest.main()
