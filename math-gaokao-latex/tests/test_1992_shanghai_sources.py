"""1992 Shanghai intake invariants; not mathematical or independent acceptance."""
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1992_上海卷"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources
sys.path.insert(0, str(ROOT.parent / "math-gaokao-2017-2026" / "tools"))
import md2tex


class Shanghai1992SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (PROJECT / "题面转录草稿.md").read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.text)
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))

    def test_fixed_manifest_identity_and_file_fingerprints(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(s for s in manifest["sources"] if s["source_id"] == self.record["source_id"])
        for key in ("upstream_path", "git_blob_oid"):
            self.assertEqual(source[key], self.record[key])
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["artifact"]["page_count"], 6)
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        for filename, expected in (("题面转录草稿.md", self.record["draft_sha256"]),
                                   ("印载答案摘录.md", self.record["source_answer_excerpt"]["sha256"])):
            self.assertEqual(hashlib.sha256((PROJECT / filename).read_bytes()).hexdigest(), expected)

    def test_all_26_question_ids_and_printed_subparts(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 27)))
        self.assertEqual({q.number: q.subparts for q in self.questions if q.subparts},
                         {24: (1, 2, 3), 25: (1, 2)})
        records = self.record["question_sources"]
        self.assertEqual([r["question_number"] for r in records], list(range(1, 27)))
        self.assertEqual(len({r["question_id"] for r in records}), 26)
        for question, record in zip(self.questions, records):
            self.assertEqual(record["question_id"], self.record["source_id"] + f":q{question.number:03d}")
            self.assertEqual(record["body_sha256"], hashlib.sha256(question.body.encode()).hexdigest())
            self.assertEqual(record["review_status"], "pending-independent-review")

    def test_printed_scores_and_type_ranges_total_150(self):
        self.assertEqual(self.record["question_scores"], [3] * 20 + [12] * 3 + [16, 18, 20])
        self.assertEqual(sum(self.record["question_scores"]), self.record["total_score"])
        self.assertEqual(self.record["total_score"], 150)
        self.assertEqual([r["score"] for r in self.record["question_type_ranges"]], [30, 30, 36, 54])
        self.assertEqual(self.record["subpart_scores"], {"24": [6, 4, 6], "25": [9, 9]})
        self.assertEqual([r["question_type"] for r in self.record["question_sources"]],
                         ["fill-in"] * 10 + ["single-choice"] * 10 + ["solution"] * 6)

    def test_choice_slots_and_math_delimiters(self):
        for question in self.questions[10:20]:
            for letter in "ABCD":
                self.assertEqual(question.body.count("（" + letter + "）"), 1)
        self.assertEqual(self.text.count("$") % 2, 0)
        self.assertEqual(self.text.count(r"\begin{cases}"), self.text.count(r"\end{cases}"))
        self.assertEqual(self.text.count("{"), self.text.count("}"))
        for question in self.questions:
            self.assertNotIn("## ", question.body)

    def test_page_regions_and_cross_page_questions(self):
        self.assertEqual([r["page"] for r in self.record["page_map"]], list(range(1, 7)))
        self.assertEqual([r["printed_page"] for r in self.record["page_map"]],
                         ["5-3", "5-4", "5-5", "5-6", "5-7", None])
        records = self.record["question_sources"]
        self.assertEqual([r["page"] for r in records[9]["regions"]], [1, 2])
        self.assertEqual([r["page"] for r in records[22]["regions"]], [2, 3])
        self.assertIn("MediaBox", self.record["bbox_coordinate_space"])
        width, height = self.record["render_page_size_pt"]
        for record in records:
            self.assertTrue(record["regions"])
            for region in record["regions"]:
                x0, y0, x1, y1 = region["bbox_pt"]
                self.assertTrue(0 <= x0 < x1 <= width)
                self.assertTrue(0 <= y0 < y1 <= height)
                self.assertIn(region["page"], (1, 2, 3))

    def test_image_verified_risk_symbols_and_q25_endpoint(self):
        self.assertIn(r"\dfrac1{x^2}", self.questions[1].body)
        self.assertIn(r"\sqrt x-1", self.questions[7].body)
        self.assertIn(r"x\ge0", self.questions[7].body)
        self.assertIn(r"x^{\frac13}", self.questions[11].body)
        self.assertIn(r"|w|\le\sqrt2", self.questions[21].body)
        self.assertIn(r"|PA|\cdot|PB|=1", self.questions[22].body)
        self.assertIn(r"0<q\le1", self.questions[24].body)
        self.assertIn(r"(1-a^2)x^2+a^2y^2-a^2=0", self.questions[25].body)
        self.assertEqual([r["question_number"] for r in self.record["confirmed_high_risk_details"]], [2, 8, 12, 5, 10])
        self.assertIn(r"(\sqrt3+i)^6", self.questions[4].body)
        self.assertNotIn(r"(\sqrt3+i)^8", self.questions[4].body)
        self.assertIn(r"$B_1M$", self.questions[9].body)
        self.assertNotIn(r"$BM$", self.questions[9].body)
        self.assertIn(r"A\!-\!SB\!-\!Q", self.questions[23].body)

    def test_printed_answers_are_not_official_and_generated_answers_are_separate(self):
        record = self.record
        self.assertTrue(record["source_has_answers"])
        self.assertTrue(record["source_has_solutions"])
        self.assertIsNone(record["official_answer"])
        generated = record["generated_solution"]
        self.assertEqual(generated["attribution"], "main-agent-derived-non-official")
        self.assertFalse(generated["independent_review"])
        self.assertNotEqual(generated["path"], record["source_answer_excerpt"]["path"])
        excerpt = record["source_answer_excerpt"]
        self.assertEqual(excerpt["question_numbers"], list(range(1, 27)))
        self.assertEqual(excerpt["choice_numbers"], list(range(11, 21)))
        self.assertEqual(excerpt["choice_key"], list("DCDDCABABB"))
        self.assertEqual(excerpt["attribution"], "source-printed-non-official-unverified-publisher")
        self.assertFalse(excerpt["solution_transcription_complete"])
        text = (PROJECT / excerpt["path"]).read_text(encoding="utf-8")
        self.assertIn(r"-2<x<2", text)
        self.assertIn(r"q=1", text)
        self.assertIn(r"\dfrac{7\pi}4,2\pi\right)", text)

    def test_printed_solution_transcription_is_complete_separate_and_flags_source_issue(self):
        transcription = self.record["printed_solution_transcription"]
        path = PROJECT / transcription["path"]
        text = path.read_text(encoding="utf-8")
        self.assertFalse(any(ord(char) < 32 and char not in "\n\r\t" for char in text))
        display_balance = 0
        for line in text.splitlines():
            if line.strip() == r"\[":
                display_balance += 1
            elif line.strip() == r"\]":
                display_balance -= 1
                self.assertGreaterEqual(display_balance, 0)
        self.assertEqual(display_balance, 0)
        self.assertEqual(text.count(r"\("), text.count(r"\)"))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), transcription["sha256"])
        self.assertEqual(transcription["source_pdf_sha256"], self.record["pdf_sha256"])
        self.assertEqual(transcription["source_pages"], [3, 4, 5, 6])
        self.assertEqual(transcription["question_numbers"], [21, 22, 23, 24, 25, 26])
        self.assertTrue(transcription["transcription_complete"])
        self.assertEqual(transcription["transcription_method"], "manual-visual-from-cached-page-renders-no-OCR")
        self.assertFalse(transcription["independent_review"])
        for number in range(21, 27):
            self.assertIn(f"### 第{number}题", text)
        self.assertIn("**解一**", text)
        self.assertIn("**解二**", text)
        self.assertIn(r"\frac{\sqrt{13}-2}{6}<k<\frac{\sqrt5-1}{4}", text)
        self.assertEqual(transcription["source_solution_issue_ids"], ["q26-alt-proof-open-bound"])
        issues = self.record["source_solution_issues"]
        self.assertEqual([issue["issue_id"] for issue in issues], ["q26-alt-proof-open-bound"])
        self.assertIn("严格不等式", issues[0]["detail"])
        self.assertFalse(self.record["source_answer_excerpt"]["solution_transcription_complete"])
        converted = md2tex.convert_markdown(
            text, md2tex.ConversionContext(figure_map={}, strict=True)
        )
        self.assertEqual(converted.warnings, ())
        self.assertEqual(converted.referenced_figures, ())

    def test_registered_figure_sources_and_canonical_links(self):
        expected = {
            10: (1, "source-faithful-projection", "f1992_shanghai_q10_prism.tex"),
            11: (2, "source-qualitative-reconstruction", "f1992_shanghai_q11_panels.tex"),
            24: (3, "source-faithful-projection", "f1992_shanghai_q24_cones.tex"),
            26: (3, "mathematical-reconstruction", "f1992_shanghai_q26_curves.tex"),
        }
        figures = self.record["figure_files"]
        self.assertEqual(self.record["question_figures_pending"], [])
        self.assertEqual([item["question_number"] for item in figures], list(expected))
        self.assertEqual(len({item["path"] for item in figures}), 4)
        questions = {question.number: question for question in self.questions}
        for item in figures:
            number = item["question_number"]
            page, classification, filename = expected[number]
            self.assertEqual(item["source_page"], page)
            self.assertEqual(item["classification"], classification)
            self.assertEqual(Path(item["path"]).name, filename)
            source_path = PROJECT / item["path"]
            self.assertTrue(source_path.is_file())
            self.assertEqual(hashlib.sha256(source_path.read_bytes()).hexdigest(), item["sha256"])
            target = f"../math-gaokao-latex/1992_上海卷/{item['path']}"
            self.assertEqual(self.text.count(f"]({target})"), 1)
            self.assertEqual(questions[number].body.count(f"]({target})"), 1)
            canonical_target = (ROOT.parent / "1992" / target).resolve()
            self.assertEqual(canonical_target, source_path.resolve())

    def test_tikz_is_self_contained_and_strict_converter_emits_each_figure(self):
        figure_map = {}
        for item in self.record["figure_files"]:
            path = PROJECT / item["path"]
            source = path.read_text(encoding="utf-8")
            self.assertEqual(source.count(r"\begin{tikzpicture}"), 1)
            self.assertEqual(source.count(r"\end{tikzpicture}"), 1)
            for forbidden in (r"\includegraphics", r"\input", r"\write18", r"\documentclass", r"\begin{document}"):
                self.assertNotIn(forbidden, source)
            target = f"../math-gaokao-latex/1992_上海卷/{item['path']}"
            figure_map[target] = path.stem

        result = md2tex.convert_markdown(
            self.text, md2tex.ConversionContext(figure_map=figure_map, strict=True)
        )
        expected_names = tuple(Path(item["path"]).stem for item in self.record["figure_files"])
        self.assertEqual(result.warnings, ())
        self.assertEqual(result.referenced_figures, expected_names)
        self.assertEqual(
            re.findall(r"\\input\{figures/([^}]+)\}", result.text), list(expected_names)
        )

    def test_q10_projection_keeps_midpoints_and_hidden_diagonal(self):
        source = (PROJECT / "figures/f1992_shanghai_q10_prism.tex").read_text(encoding="utf-8")

        def coordinate(name):
            match = re.search(rf"\\coordinate \({name}\) at \(([^,]+),([^)]+)\);", source)
            self.assertIsNotNone(match, name)
            return tuple(float(value) for value in match.groups())

        def midpoint(first, second):
            return tuple((a + b) / 2 for a, b in zip(first, second))

        for actual, first, second in (("E", "A1", "B1"), ("F", "A", "A1"),
                                      ("M", "A", "C"), ("M", "B", "D")):
            for got, want in zip(coordinate(actual), midpoint(coordinate(first), coordinate(second))):
                self.assertTrue(math.isclose(got, want, abs_tol=1e-12))
        self.assertRegex(source, r"\\draw\[dashed\] \(B1\)--\(M\)")

    def test_q11_panels_preserve_option_directions_and_parameter_consistency(self):
        source = (PROJECT / "figures/f1992_shanghai_q11_panels.tex").read_text(encoding="utf-8")
        match = re.search(r"\\foreach \\panel/\\shift/\\growth/\\opening in \{([^}]+)\}", source)
        self.assertIsNotNone(match)
        panels = {}
        for item in match.group(1).split(","):
            panel, _shift, growth, opening = item.split("/")
            panels[panel] = (int(growth), int(opening))
        self.assertEqual(panels, {"A": (1, 1), "B": (-1, 1), "C": (1, -1), "D": (-1, -1)})
        self.assertIn(r"plot (\x,{.6*pow(2,\growth*\x)})", source)
        self.assertIn(r"plot (\x,{\opening*.3*\x*\x})", source)
        # y=1 is drawn at .6; for D's displayed a=1/2, .6(a-1)=-.3.
        self.assertAlmostEqual(.6 * (.5 - 1), -.3)
        self.assertIn(r"\ifnum\opening=1", source)

    def test_q24_cone_foot_matches_projection_geometry(self):
        source = (PROJECT / "figures/f1992_shanghai_q24_cones.tex").read_text(encoding="utf-8")
        self.assertIn(r"\coordinate (C) at (.375,{-.1*sqrt(3)})", source)
        self.assertIn(r"\coordinate (H) at (.3,{.3-.08*sqrt(3)})", source)
        self.assertRegex(source, r"\\draw\[dashed\] \(S\)--\(C\) \(O\)--\(C\) \(O\)--\(H\)")

        root3 = math.sqrt(3)
        s = (0.0, 0.0, 1.0)
        c = (0.25, -root3 / 4, 0.0)
        vector = tuple(c[i] - s[i] for i in range(3))
        h = (0.2, -root3 / 5, 0.2)
        self.assertTrue(math.isclose(sum(h[i] * vector[i] for i in range(3)), 0, abs_tol=1e-12))
        for got, want in zip((1.5 * h[0], .4 * h[1] + 1.5 * h[2]), (.3, .3 - .08 * root3)):
            self.assertTrue(math.isclose(got, want, abs_tol=1e-12))

    def test_q26_reconstruction_is_a_legal_example_not_a_question_condition(self):
        source = (PROJECT / "figures/f1992_shanghai_q26_curves.tex").read_text(encoding="utf-8")
        question = next(q for q in self.questions if q.number == 26)
        m = (3 + math.sqrt(5)) / 2
        self.assertIn("a=2", source)
        self.assertNotIn("a=2", question.body)
        self.assertTrue(math.isclose(m * m - 3 * m + 1, 0, abs_tol=1e-12))
        x, y = -2.0, 2.0
        self.assertTrue(math.isclose(y, -x, abs_tol=1e-12))
        self.assertTrue(math.isclose(y * y, 1 + .75 * x * x, abs_tol=1e-12))
        self.assertTrue(math.isclose(m - x * x / (4 * (m - 1)), y, abs_tol=1e-12))
        self.assertTrue(math.isclose(m - (m - 1), 1, abs_tol=1e-12))

    def test_missing_figures_and_independent_checks_block_acceptance(self):
        self.assertIsNone(self.record["paper_id"])
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        pending = [q.number for q in self.questions if "题图待重绘" in q.body]
        self.assertEqual(pending, [])
        self.assertEqual(pending, self.record["question_figures_pending"])
        visual = self.record["figure_smoke_review"]
        self.assertEqual(visual["compiler_exit_code"], 0)
        self.assertEqual(visual["page_count"], 1)
        self.assertEqual(visual["page_size"], "A4")
        self.assertEqual(visual["diagnostics"], [])
        self.assertFalse(visual["independent_review"])
        self.assertFalse(visual["formal_receipt"])
        for suffix in ("png", "jpg", "jpeg"):
            self.assertFalse(list(PROJECT.rglob("*." + suffix)))

    def test_resume_uses_cached_ocr_but_never_certifies_math(self):
        ocr = self.record["ocr"]
        self.assertEqual(ocr["first_run"]["ocr_calls"], 3)
        self.assertEqual(ocr["resume_check"]["ocr_calls"], 0)
        self.assertEqual(ocr["resume_check"]["cache_hits"], 3)
        self.assertEqual(ocr["resume_check"]["render_cache_hits"], 3)
        self.assertEqual(ocr["status"], "recognized_unverified")
        self.assertEqual(len(self.record["render"]), 6)
        for render in self.record["render"]:
            path = Path(render["path"])
            self.assertFalse(path.is_absolute())
            self.assertNotIn("..", path.parts)
            self.assertEqual(path.parts[0], ".work")
            self.assertFalse(render["independent_review"])
            self.assertRegex(render["sha256"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
