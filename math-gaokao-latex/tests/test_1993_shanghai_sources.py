"""1993 Shanghai source-bound transcription checks; not final acceptance."""
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1993_上海卷"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources
sys.path.insert(0, str(ROOT.parent / "math-gaokao-2017-2026" / "tools"))
import md2tex

SOURCE_ID = "src-7f02648c0c540aea2ea527ac2eedf30b9aea0afc501f47280e74b2970532ef88"
SOURCE_SHA256 = "361e60798105e9ccea1b98f8b80985f2ba1204ba2914506da0055cd30228c0f8"


class Shanghai1993SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.question_path = PAPER / "题面转录草稿.md"
        cls.answer_path = PAPER / "印载答案摘录.md"
        cls.record_path = PAPER / "来源校对.json"
        cls.question_text = (
            cls.question_path.read_text(encoding="utf-8")
            if cls.question_path.is_file()
            else ""
        )
        cls.questions = (
            solution_sources.parse_question_blocks(cls.question_text)
            if cls.question_text
            else []
        )
        cls.record = (
            json.loads(cls.record_path.read_text(encoding="utf-8"))
            if cls.record_path.is_file()
            else {}
        )

    def setUp(self):
        required = [self.question_path, self.answer_path, self.record_path]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
        self.assertFalse(missing, "transcription artifacts not created yet: " + ", ".join(missing))

    def test_fixed_manifest_identity_and_source_fingerprints(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(item for item in manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 7)
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["pdf_sha256"], SOURCE_SHA256)
        self.assertEqual(self.record["upstream_path"], "普通高考/1993/1993上海.pdf")
        for artifact in (self.record["question_draft"], self.record["source_answer_excerpt"]):
            digest = hashlib.sha256((PAPER / artifact["path"]).read_bytes()).hexdigest()
            self.assertEqual(artifact["sha256"], digest)

    def test_question_coverage_and_truncated_q23_are_explicit(self):
        self.assertEqual([question.number for question in self.questions], list(range(1, 27)))
        q23 = self.questions[22].body
        self.assertIn("题面截断", q23)
        self.assertNotIn(r"y=x-1", q23)
        self.assertEqual(self.record["question_count"], 26)
        self.assertEqual(self.record["question_sources"][22]["transcription_status"], "source-truncated")
        self.assertEqual(self.record["transcription_status"], "incomplete-source-gap-q23")

    def test_question_types_scores_and_subparts_match_printed_structure(self):
        self.assertEqual(
            [item["question_type"] for item in self.record["question_sources"]],
            ["fill-in"] * 10 + ["single-choice"] * 10 + ["solution"] * 6,
        )
        self.assertEqual(self.record["question_scores"], [3] * 20 + [12, 12, 12, 16, 18, 20])
        self.assertEqual(sum(self.record["question_scores"]), 150)
        self.assertEqual(self.record["subpart_scores"], {"24": [5, 5, 6], "25": [5, 5, 8], "26": [6, 8, 6]})

    def test_high_risk_source_symbols_and_q3_conjugate_are_preserved(self):
        self.assertIn(r"\bar z", self.questions[2].body)
        self.assertIn(r"\cos\dfrac{7\pi}{5}", self.questions[2].body)
        self.assertIn(r"(x-1)^9", self.questions[11].body)
        self.assertIn(r"x^3", self.questions[12].body)
        self.assertIn(r"\rho\sin\theta=2", (PAPER / "印载答案摘录.md").read_text(encoding="utf-8"))

    def test_source_answers_are_separate_from_official_and_generated_answers(self):
        answer_text = (PAPER / "印载答案摘录.md").read_text(encoding="utf-8")
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["source_answer_excerpt"]["attribution"], "source-printed-unverified-publisher")
        self.assertEqual(self.record["source_answer_excerpt"]["question_numbers"], list(range(1, 21)))
        self.assertEqual(self.record["generated_solution"]["attribution"], "not-created")
        self.assertFalse(self.record["generated_solution"]["independent_review"])
        self.assertIn("第23题", answer_text)
        self.assertIn("不绑定为一份完整题目的答案", answer_text)

    def test_stage_notes_point_to_completed_transcription_without_reclassifying_q10(self):
        self.assertIn("填空题第10题", self.question_text.split("## 一、", 1)[0])
        answer_text = self.answer_path.read_text(encoding="utf-8")
        self.assertNotIn("完整印载推导尚未转录", answer_text)
        self.assertIn("[印载解析转录](印载解析转录.md)", answer_text)
        self.assertTrue((PAPER / "印载解析转录.md").is_file())

    def test_printed_solution_transcription_is_complete_but_q23_remains_unbound(self):
        artifact = self.record["printed_solution_transcription"]
        self.assertEqual(artifact["path"], "印载解析转录.md")
        self.assertEqual(artifact["question_numbers"], list(range(21, 27)))
        self.assertTrue(artifact["transcription_complete"])
        self.assertEqual(artifact["q23_binding_status"], "withheld-source-question-truncated")
        transcript_path = PAPER / artifact["path"]
        transcript = transcript_path.read_text(encoding="utf-8")
        self.assertEqual(artifact["sha256"], hashlib.sha256(transcript_path.read_bytes()).hexdigest())
        for number in range(21, 27):
            self.assertIn(f"## 第{number}题", transcript)
        q23 = re.search(r"(?ms)^## 第23题.*?(?=^## |\Z)", transcript)
        self.assertIsNotNone(q23)
        self.assertIn("题面截断", q23.group(0))
        self.assertIn("不绑定", q23.group(0))
        self.assertEqual(self.record["question_sources"][22]["transcription_status"], "source-truncated")
        self.assertEqual(artifact["source_pages"], [4, 5, 6, 7])
        self.assertEqual(artifact["source_pdf_sha256"], SOURCE_SHA256)
        self.assertEqual(artifact["attribution"], "source-printed-solutions-unverified-publisher")
        self.assertFalse(artifact["independent_review"])

        progress = (ROOT / "PROGRESS.md").read_text(encoding="utf-8")
        stage = re.search(
            r"(?ms)^## 1993 上海卷：第21—26题印载解析逐页转录.*?(?=^## |\Z)",
            progress,
        )
        self.assertIsNotNone(stage, "PROGRESS.md must record this completed transcription stage")
        for required in ("已完成：", "修改文件：", "验证：", "成本与质量边界：", "剩余/下一步："):
            self.assertIn(required, stage.group(0))
        self.assertIn("Q23", stage.group(0))
        self.assertIn("整卷仍未完成", stage.group(0))

    def test_q23_source_search_lead_is_not_misrepresented_as_recovered_source(self):
        source_note = (PAPER / "核源记录.md").read_text(encoding="utf-8")
        section = re.search(r"(?ms)^## Q23同版本来源追索补充.*?(?=^## |\Z)", source_note)
        self.assertIsNotNone(section)
        self.assertIn("756310352X", section.group(0))
        self.assertIn("8517858", section.group(0))
        self.assertIn("仅作获取线索，不作转录依据", section.group(0))
        self.assertIn("no matching result", section.group(0))
        self.assertIn("不证明图书不存在", section.group(0))
        self.assertEqual(self.record["question_sources"][22]["transcription_status"], "source-truncated")
        self.assertEqual(
            self.record["printed_solution_transcription"]["q23_binding_status"],
            "withheld-source-question-truncated",
        )

        progress = (ROOT / "PROGRESS.md").read_text(encoding="utf-8")
        stage = re.search(
            r"(?ms)^## 1993 上海卷：Q23同版本来源追索与候选判定.*?(?=^## |\Z)",
            progress,
        )
        self.assertIsNotNone(stage, "PROGRESS.md must preserve the unresolved source-search result")
        self.assertIn("未恢复题面", stage.group(0))
        self.assertIn("不据目录或印载解析补写题面", stage.group(0))

    def test_question_source_ids_pages_and_body_hashes_are_stable(self):
        source_rows = self.record["question_sources"]
        self.assertEqual(len(source_rows), 26)
        self.assertEqual(len({row["question_id"] for row in source_rows}), 26)
        for question, row in zip(self.questions, source_rows):
            self.assertEqual(row["question_number"], question.number)
            self.assertEqual(row["question_id"], SOURCE_ID + f":q{question.number:03d}")
            self.assertEqual(row["body_sha256"], hashlib.sha256(question.body.encode()).hexdigest())
            self.assertTrue(row["source_pages"])
            expected_review = "needs-source-recovery" if question.number == 23 else "pending-independent-review"
            self.assertEqual(row["review_status"], expected_review)

    def test_external_preview_mismatch_and_no_raster_assets_are_recorded(self):
        source_note = (PAPER / "核源记录.md").read_text(encoding="utf-8")
        self.assertIn("结构明显不同", source_note)
        self.assertIn("未用于补题、校正或合并", source_note)
        image_files = [
            path
            for suffix in ("*.png", "*.jpg", "*.jpeg")
            for path in PAPER.rglob(suffix)
            if ".work" not in path.relative_to(PAPER).parts
        ]
        self.assertEqual(image_files, [])

    def test_progress_records_stage_result_and_remaining_gates(self):
        progress = (ROOT / "PROGRESS.md").read_text(encoding="utf-8")
        match = re.search(
            r"(?ms)^## 1993 上海卷：题面与答案摘录阶段稿落盘.*?(?=^## |\Z)",
            progress,
        )
        self.assertIsNotNone(match, "PROGRESS.md must record the completed transcription stage")
        section = match.group(0)
        for required in ("已完成：", "修改文件：", "验证：", "成本与质量边界：", "剩余/下一步："):
            self.assertIn(required, section)
        self.assertIn("Q23", section)
        self.assertIn("整卷转录尚未完成", section)

        figure_stage = re.search(
            r"(?ms)^## 1993 上海卷：四组题图矢量稿与单卷试编.*?(?=^## |\Z)",
            progress,
        )
        self.assertIsNotNone(figure_stage, "PROGRESS.md must record the separate figure stage")
        for required in ("Q10", "Q11", "Q24", "Q26", "修改文件：", "验证：", "剩余/下一步："):
            self.assertIn(required, figure_stage.group(0))
        self.assertIn("整卷转录未完成", figure_stage.group(0))

    def test_registered_figure_sources_link_to_self_contained_tikz(self):
        expected = {
            10: (2, "source-faithful-projection", "f1993_shanghai_q10_cube.tex"),
            11: (2, "source-qualitative-reconstruction", "f1993_shanghai_q11_graphs.tex"),
            24: (3, "source-faithful-schematic-reconstruction", "f1993_shanghai_q24_dihedral.tex"),
            26: (4, "mathematical-reconstruction", "f1993_shanghai_q26_ellipse_hyperbola.tex"),
        }
        figures = self.record.get("figure_files", [])
        self.assertEqual(self.record.get("question_figures_pending"), [])
        self.assertEqual([item["question_number"] for item in figures], list(expected))
        self.assertEqual(len({item["path"] for item in figures}), 4)
        questions = {question.number: question for question in self.questions}
        figure_map = {}
        for item in figures:
            number = item["question_number"]
            page, classification, filename = expected[number]
            self.assertEqual(item["source_page"], page)
            self.assertEqual(item["classification"], classification)
            self.assertEqual(Path(item["path"]).name, filename)
            source_path = PAPER / item["path"]
            self.assertTrue(source_path.is_file())
            self.assertEqual(hashlib.sha256(source_path.read_bytes()).hexdigest(), item["sha256"])
            target = item["path"]
            self.assertEqual(self.question_text.count(f"]({target})"), 1)
            self.assertEqual(questions[number].body.count(f"]({target})"), 1)
            source = source_path.read_text(encoding="utf-8")
            self.assertEqual(source.count(r"\begin{tikzpicture}"), 1)
            self.assertEqual(source.count(r"\end{tikzpicture}"), 1)
            for forbidden in (r"\includegraphics", r"\input", r"\write18", r"\documentclass", r"\begin{document}"):
                self.assertNotIn(forbidden, source)
            figure_map[target] = source_path.stem

        converted = md2tex.convert_markdown(
            self.question_text,
            md2tex.ConversionContext(figure_map=figure_map, strict=True),
        )
        expected_names = tuple(Path(item["path"]).stem for item in figures)
        self.assertEqual(converted.warnings, ())
        self.assertEqual(converted.referenced_figures, expected_names)


if __name__ == "__main__":
    unittest.main()
