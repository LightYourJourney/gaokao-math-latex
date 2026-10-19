"""Deterministic question IR export reuses registered transcription evidence."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from export_question_ir import QuestionIRExportError, build_question_ir


PAPER_ID = "gk-2017-regular-national-1-science"


class QuestionIRExportTests(unittest.TestCase):
    def test_registered_paper_exports_stable_question_data_without_claiming_official_answers(self):
        document = build_question_ir(ROOT.parent.parent.parent, PAPER_ID)

        self.assertEqual(document["paper_id"], PAPER_ID)
        self.assertEqual(document["source"]["sha256"], "0f283c36559ea6d249f57acf32e37507ae546c1521ed5b38b13cbe116f4a203e")
        self.assertEqual(len(document["questions"]), 23)
        self.assertEqual(
            [row["question_id"] for row in document["questions"]],
            [f"{PAPER_ID}-q{number:02d}" for number in range(1, 24)],
        )
        self.assertEqual(document, build_question_ir(ROOT.parent.parent.parent, PAPER_ID))
        first = document["questions"][0]
        self.assertEqual(first["question_id"], "gk-2017-regular-national-1-science-q01")
        self.assertEqual(first["question_number"], 1)
        self.assertEqual(first["source_pages"], [1])
        self.assertIn("\n", first["body_markdown"])
        self.assertIsNone(first["source_bbox"])
        self.assertIsNone(first["official_answer"])
        self.assertEqual(first["answer_evidence"]["origin"], "project-answer-evidence")
        self.assertEqual(first["transcription_review"]["result"], "passed")
        self.assertIsNone(first["options"])
        self.assertIsNone(first["equations"])
        self.assertEqual(document["questions"][1]["figures"], ["images/2017理-t2-太极图.png"])

    def test_export_rejects_question_text_that_no_longer_matches_provenance(self):
        repo = ROOT.parent.parent.parent
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = Path(temp_dir)
            project = copy_root / "math-gaokao-latex"
            (project / "2017_全国Ⅰ卷_理科").mkdir(parents=True)
            questions_path = copy_root / "2017/2017_数学真题_理_试题.md"
            questions_path.parent.mkdir(parents=True)
            shutil.copy2(repo / "math-gaokao-latex/source-manifest.json", project)
            shutil.copy2(ROOT / "2017_全国Ⅰ卷_理科/provenance.json", project / "2017_全国Ⅰ卷_理科")
            shutil.copy2(repo / "2017/2017_数学真题_理_试题.md", questions_path)
            questions_text = questions_path.read_text(encoding="utf-8")
            questions_path.write_text(questions_text.replace("$A=", "$AA=", 1), encoding="utf-8")

            with self.assertRaisesRegex(QuestionIRExportError, "题面哈希与 provenance 不一致"):
                build_question_ir(copy_root, PAPER_ID)

    def test_export_rejects_unknown_paper_id(self):
        with self.assertRaisesRegex(QuestionIRExportError, "未找到唯一试卷记录"):
            build_question_ir(ROOT.parent.parent.parent, "not-a-paper")


if __name__ == "__main__":
    unittest.main()
