import csv
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
PAPER_ID = "gk-1990-regular-national-science"
SOURCE_ID = "src-9c2fc92cdbbeac0484bf7355db2d32805c316e1a7be74e3bf175a3891a167a49"
SOURCE_SHA256 = "7801e6dab50ca58eabdc74d074cdaa7012cdee873dcc5304e0df37248986b43a"
PAPER_DIR = PROJECT / "1990_全国卷_理科"
QUESTION_ID_Q20 = f"{PAPER_ID}-q20"

sys.path.insert(0, str(PROJECT / "tools"))
import make_editions
import provenance
import solution_sources


class NationalScience1990SourceRegistrationTests(unittest.TestCase):
    def test_registration_provenance_and_four_entrypoints_are_current(self):
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        paper = next((item for item in manifest["papers"] if item["paper_id"] == PAPER_ID), None)
        self.assertIsNotNone(paper, "1990 全国理科须经来源门禁后登记为独立 canonical 卷")

        source = next(item for item in manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["paper_relation"], "canonical")
        self.assertEqual(source["paper_id"], PAPER_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(paper["production_state"], "blocked")
        self.assertIn("出版社与版次未认证", paper["index_metadata"]["note"])

        batch_id = "phase4-b13"
        batch = next(item for item in manifest["batches"] if item["batch_id"] == batch_id)
        self.assertEqual(batch["paper_ids"], [PAPER_ID])
        self.assertTrue(paper["issue_ids"], "未解决的 Q20 体积标签歧义必须阻止正式放行")

        index = json.loads((PROJECT / "index.json").read_text(encoding="utf-8"))
        index_paper = next(item for item in index["papers"] if item["id"] == PAPER_ID)
        self.assertEqual(index_paper["paper_id"], PAPER_ID)
        self.assertIn("出版社与版次未认证", index_paper["note"])

        csv_path = PROJECT / "manifest.csv"
        with csv_path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        source_row = next(row for row in rows if row.get("source_id") == SOURCE_ID)
        self.assertEqual(source_row.get("paper_id"), PAPER_ID)

        provenance_path = PAPER_DIR / "provenance.json"
        document = json.loads(provenance_path.read_text(encoding="utf-8"))
        self.assertEqual(document["paper_id"], PAPER_ID)
        self.assertEqual(document["batch_id"], batch_id)
        self.assertEqual(len(document["questions"]), 26)
        reviewer_role = document["questions"][0]["reviewer_role"]
        self.assertIn("Q1-13", reviewer_role)
        self.assertIn("Q14-25", reviewer_role)
        self.assertIn("supplemental Q5 and Q26", reviewer_role)
        self.assertTrue(
            all(item["reviewer_role"] == reviewer_role for item in document["questions"])
        )
        provenance.validate_provenance(document, manifest, ROOT, recompute=True)

        q20 = document["questions"][19]
        self.assertEqual(q20["question_id"], QUESTION_ID_Q20)
        self.assertEqual(q20["source_ref"]["source_id"], SOURCE_ID)
        self.assertEqual(q20["source_sha256"], SOURCE_SHA256)
        self.assertEqual(q20["answer_evidence"]["grade"], "U")
        self.assertTrue(q20["issue_ids"])
        self.assertEqual(set(q20["issue_ids"]), set(paper["issue_ids"]))
        self.assertTrue(
            all(
                item["answer_evidence"]["grade"] == "A"
                for item in document["questions"]
                if item["question_order"] != 20
            )
        )
        self.assertTrue(
            all(item["transcription_review"]["result"] == "passed" for item in document["questions"])
        )

        answer_key = (ROOT / "1990/1990_数学真题_全国理_答案要点.md").read_text(encoding="utf-8")
        self.assertIn("official_answer: null", answer_key)
        self.assertIn("非官方答案", answer_key)
        questions = (ROOT / "1990/1990_数学真题_全国理_试题.md").read_text(encoding="utf-8")
        solution_body = (ROOT / "1990/1990_数学真题_全国理_解析正文.md").read_text(encoding="utf-8")
        combined = (ROOT / "1990/1990_数学真题_全国理_含解析.md").read_text(encoding="utf-8")
        self.assertEqual(combined, solution_sources.render_combined(questions, solution_body, answer_key))

        shells = make_editions.build_shells(
            make_editions.load_templates(ROOT), make_editions.paper_shell(paper)
        )
        self.assertEqual(len(shells), 4)
        for relative, expected in shells.items():
            with self.subTest(entrypoint=relative):
                self.assertEqual((ROOT / relative).read_bytes(), expected)


if __name__ == "__main__":
    unittest.main()
