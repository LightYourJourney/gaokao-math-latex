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


def _figure_coordinates(source):
    return {
        name: (float(x), float(y))
        for name, x, y in re.findall(
            r"\\coordinate\s+\(([^)]+)\)\s+at\s+\(([^,]+),([^)]+)\);", source
        )
    }


def _figure_drawn_edges(source):
    edges = {}
    draw_commands = re.findall(r"\\draw(?:\[([^\]]*)\])?\s*(.*?);", source, re.DOTALL)
    for options, path in draw_commands:
        style = {part.strip() for part in options.split(",") if part.strip()}
        for first, second in re.findall(r"(?=\(([^()]+)\)\s*--\s*\(([^()]+)\))", path):
            edge = tuple(sorted((first.strip(), second.strip())))
            edges.setdefault(edge, []).append(style)
    return edges


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
        index_note = self.paper["index_metadata"]["note"]
        self.assertIn("Q25项目推导已独立复核", index_note)
        self.assertIn("其余25题仍待复核", index_note)
        self.assertNotIn("Q25答案与解析保持待核", index_note)
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
            r"\sin 2x-2\cos^2x",
            r"\sin 2x+\sin\left(2x+\frac\pi3\right)",
            r"\cos 2x+\cos\left(2x+\frac\pi3\right)",
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
        self.assertIn("原印载分段遗漏", self.answers)
        self.assertIn("Q25", self.answers)
        self.assertEqual(self.record["review_status"], "needs-review")

    def test_q1_to_q10_source_transcriptions_and_short_answers_are_reviewed(self):
        reviewed = {
            item["question_number"]: item
            for item in self.record["question_sources"]
        }
        checks = {
            item["question_id"]: item
            for item in self.record.get("derived_solution_checks", [])
        }
        expected = {
            1: ("-2<x<0", "absolute-value-inequality", ()),
            2: (r"\dfrac{\sqrt7}{4}", "principal-half-angle-identity", ()),
            3: (r"(x+2)^2+(y-3)^2=4", "distance-from-center-to-y-axis", ()),
            4: ("x=4", "logarithm-domain-and-base-change", ()),
            5: (
                "24",
                "cone-total-surface-area-cost",
                ("r=5", "l=10", "πr²+πrl=25π+50π=75π", "π=3.2", "75×3.2=240", "0.10×240=24"),
            ),
            6: (
                r"y=-\sqrt{x^2+1}\ (x\ge0)",
                "inverse-function-domain-range",
                ("x≤-1", "y≥0", "x≥0"),
            ),
            7: (
                r"(0,\sqrt3),(0,-\sqrt3)",
                "standard-vertical-hyperbola-foci",
                ("a^2=2", "b^2=1", "c^2=a^2+b^2=3", "(0,±√3)"),
            ),
            8: (
                "40",
                "binomial-expansion-exponent-match",
                (
                    r"T_{k+1}=\binom{5}{k}(x^3)^{5-k}(-2x^{-2})^k",
                    "15-5k=5",
                    "k=2",
                    r"\binom{5}{2}(-2)^2=40",
                ),
            ),
            9: (
                r"\sqrt2-1",
                "trigonometric-linear-combination-maximum",
                (
                    "2cos^2x=1+cos2x",
                    "sin2x−cos2x−1=√2sin(2x−π/4)−1",
                    "√2−1",
                ),
            ),
            10: (
                r"\dfrac\pi2",
                "sum-to-product-tangent-period",
                (
                    "2sin(2x+π/6)cos(π/6)",
                    "2cos(2x+π/6)cos(π/6)",
                    "tan(2x+π/6)",
                    "分母非零",
                    "x≠π/6+kπ/2",
                    "分子不为零",
                    "T=π/2",
                ),
            ),
        }
        for number, (answer, method, derivation_fragments) in expected.items():
            with self.subTest(question=number):
                self.assertIn(number, reviewed, f"Q{number} source review is not recorded")
                item = reviewed[number]
                self.assertEqual(item["review_status"], "source-checked")
                self.assertEqual(item["source_pages"], [1])
                self.assertEqual(
                    item["source_review"]["source_sha256"],
                    self.source["artifact"]["sha256"],
                )
                self.assertEqual(
                    item["source_review"]["method"],
                    "visual comparison against the pinned fixed scan",
                )
                self.assertIn("matches the source scan", item["source_review"]["result"])

                check = checks[f"{SOURCE_ID}:q{number:03d}"]
                self.assertEqual(check["method"], method)
                self.assertEqual(check["derived_answer"], answer)
                self.assertEqual(check["source_printed_answer"], answer)
                for fragment in derivation_fragments:
                    with self.subTest(derivation_fragment=fragment):
                        self.assertIn(fragment, check["derivation"])
                self.assertEqual(check["source_answer_page"], 3)
                self.assertEqual(check["status"], "derived-independently-reviewed")
                self.assertTrue(check["independent_review"])
                self.assertEqual(
                    check["independent_review_details"]["method"],
                    "blind solution from the question text only; printed answer withheld",
                )
                self.assertIn(
                    "independently derived",
                    check["independent_review_details"]["result"],
                )
                self.assertIsNone(check["official_answer"])

        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(self.paper["production_state"], "blocked")
        self.assertIsNone(self.record["official_answer"])

    def test_q25_coordinate_derivation_is_independently_reviewed_but_not_official(self):
        checks = self.record.get("derived_solution_checks", [])
        check = next(item for item in checks if item["question_id"].endswith(":q025"))
        self.assertEqual(check["status"], "derived-independently-reviewed")
        self.assertTrue(check["independent_review"])
        self.assertEqual(
            check["independent_review_details"]["method"],
            "blind derivation from the question crop only; printed solution and primary derivation withheld",
        )
        self.assertIn("independently derived the same", check["independent_review_details"]["result"])
        self.assertIsNone(check["official_answer"])
        self.assertEqual(check["jacobian"], "2(1+t^2)")
        self.assertEqual(check["piecewise_area"], "2(1-t+t^2-t^3) for 0<t<=1/2; (t+1/t)/2 for t>=1/2")
        self.assertEqual(check.get("first_branch_derivative"), "2(-1+2t-3t^2)<0 (discriminant -8)")
        self.assertEqual(check["monotonicity"], "decreasing on (0,1]; increasing on [1,+infinity)")
        self.assertIn("打印答案的第二支 t>=2", check["source_conflict"])
        self.assertEqual(self.record["official_answer"], None)
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertEqual(self.paper["production_state"], "blocked")

    def test_q25_project_answer_and_generated_editions_preserve_source_boundary(self):
        self.assertIn(
            "第 21—24、26 题参照固定来源印载解答整理；第 25 题依据题面推导并经独立盲核",
            self.combined,
        )
        normalized_answers = re.sub(r"\s+", "", self.answers)
        self.assertIn(r"答案：$S(t)=\begin{cases}2(1-t+t^2-t^3),&0<t<\dfrac12", normalized_answers)
        self.assertIn(r"\dfrac12\left(t+\dfrac1t\right),&t\ge\dfrac12", normalized_answers)
        self.assertIn("固定来源原印载分段（原文保留）", normalized_answers)
        self.assertIn(r"\dfrac12\left(t+\dfrac1t\right),&t\ge2", normalized_answers)
        self.assertIn(re.sub(r"\s+", "", "$S(t)$ 在 $(0,1]$ 上递减、在 $[1,+\\infty)$ 上递增"), normalized_answers)

        answers_tex = (PROJECT_DIR / "answers.tex").read_text(encoding="utf-8")
        short_tex = (PROJECT_DIR / "answers_short.tex").read_text(encoding="utf-8")
        self.assertIn(r"\gkanswer{答案（1）：$S(t)=\begin{cases}2(1-t+t^2-t^3),&0<t<\dfrac12", answers_tex)
        self.assertIn(r"\dfrac12\left(t+\dfrac1t\right),&t\ge\dfrac12", answers_tex)
        self.assertIn(r"经独立盲核", answers_tex)
        self.assertIn(r"0<t<\dfrac12", short_tex)
        self.assertIn("$t\\ge2$", short_tex)
        self.assertNotIn("t≥2", short_tex)
        self.assertIn("第25题项目推导经独立盲核", short_tex)
        self.assertIn("整卷其余内容尚未经过异人盲核", short_tex)
        self.assertIn(r"\textbf{非官方标准答案}", short_tex)

    def test_q11_origin_labels_follow_the_scanned_option_positions(self):
        figure = (PROJECT_DIR / "figures/f1994_shanghai_q11_graph_options.tex").read_text(encoding="utf-8")
        match = re.search(r"\\foreach.*?\s+in\s*\{(.*?)\}\s*\{", figure, re.DOTALL)
        self.assertIsNotNone(match)
        positions = {}
        for row in match.group(1).split(","):
            fields = [field.strip() for field in row.split("/")]
            if len(fields) >= 6:
                positions[fields[2]] = fields[5]
        self.assertEqual(positions, {"A": "right", "B": "left", "C": "right", "D": "left"})
        self.assertIn(r"\node[below \originplace] at (0,0)", figure)

    def test_q23_vector_preserves_parallel_edges_projection_and_hidden_line(self):
        figure = (PROJECT_DIR / "figures/f1994_shanghai_q23_problem.tex").read_text(encoding="utf-8")
        coordinates = _figure_coordinates(figure)
        ax, ay = coordinates["A"]
        bx, by = coordinates["B"]
        cx, cy = coordinates["C"]
        dx, dy = coordinates["D"]
        px, _ = coordinates["P"]
        self.assertGreater(ax, bx, "source projection places A to the right of B")
        self.assertLess(px, ax, "source projection places P to the left of A")
        ad = (dx - ax, dy - ay)
        bc = (cx - bx, cy - by)
        self.assertAlmostEqual(ad[0] * bc[1] - ad[1] * bc[0], 0, places=8)

        edges = _figure_drawn_edges(figure)
        self.assertEqual(edges[tuple(sorted(("A", "D")))], [{"dashed"}])
        self.assertEqual(edges[tuple(sorted(("A", "P")))], [{"dashed"}])
        for edge in (("B", "P"), ("C", "P"), ("D", "P"), ("B", "C"), ("C", "D")):
            with self.subTest(edge=edge):
                self.assertIn(tuple(sorted(edge)), edges)
                self.assertTrue(all("dashed" not in style for style in edges[tuple(sorted(edge))]))

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
