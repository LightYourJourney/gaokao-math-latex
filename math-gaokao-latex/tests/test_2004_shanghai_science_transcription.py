import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER_DIR = PROJECT / "2004_上海卷_理科"
TRANSCRIPT = ROOT / "2004/2004_数学真题_上海理_试题.md"
SOURCE_ID = "src-f8969b851ca75536af43f98ea865a04b66de9068f24bdec2c3790cd1351bed0a"
SOURCE_SHA256 = "9f6c7f71c18bcdc3dd863fc846636661eacc03b4d3837feeaafcd36258c2be5e"
PAPER_ID = "gk-2004-regular-shanghai-science"

sys.path.insert(0, str(PROJECT / "tools"))
import provenance


class ShanghaiScience2004TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        cls.index_doc = json.loads((PROJECT / "index.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription draft must exist")
        self.transcript = TRANSCRIPT.read_text(encoding="utf-8")

    def test_fixed_source_fingerprint_is_formally_bound_with_limits_preserved(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["raw_paper_name"], "2004上海理.pdf")
        self.assertEqual(source["upstream_path"], "普通高考/2004/2004上海理.pdf")
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["paper_id"], PAPER_ID)
        self.assertEqual(source["paper_relation"], "canonical")

        paper = next(item for item in self.manifest["papers"] if item["paper_id"] == PAPER_ID)
        self.assertEqual(paper["legacy_ids"], [])
        self.assertEqual(paper["source_ids"], [SOURCE_ID])
        self.assertEqual(paper["question_count"], 22)
        self.assertEqual(paper["year"], 2004)
        self.assertEqual(paper["track"], "science")
        self.assertEqual(paper["production_state"], "blocked")
        self.assertTrue({"ISSUE-1386", "ISSUE-1387"}.issubset(set(paper["issue_ids"])))

        batch = next(item for item in self.manifest["batches"] if item["batch_id"] == "phase4-b46")
        self.assertEqual(batch["status"], "closed_with_blockers")
        self.assertEqual(batch["paper_ids"], [PAPER_ID])

        manifest_csv = (PROJECT / "manifest.csv").read_text(encoding="utf-8")
        self.assertIn(f",{SOURCE_ID},", manifest_csv)
        self.assertIn(f",{SOURCE_SHA256},", manifest_csv)
        self.assertIn(PAPER_ID, manifest_csv)

        self.assertIn(SOURCE_ID, self.transcript)
        self.assertIn(SOURCE_SHA256, self.transcript)
        self.assertIn(PAPER_ID, self.transcript)

    def test_transcription_covers_all_22_questions_in_source_order(self):
        numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("## 一、填空题"), 1)
        self.assertEqual(self.transcript.count("## 二、选择题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertEqual(self.transcript.count("$") % 2, 0)

        # 验证解答题小问结构完整
        self.assertIn("(1) 求 $A$", self.transcript)
        self.assertIn("(2) 若 $B \\subseteq A$", self.transcript)
        self.assertIn("(1) 求函数 $f(x)$ 的表达式", self.transcript)
        self.assertIn("(2) 证明：当 $a > 3$ 时", self.transcript)
        self.assertIn("(1) 证明：$P - ABC$ 为正四面体", self.transcript)
        self.assertIn("(2) 若 $PD = \\dfrac{1}{2}PA$", self.transcript)
        self.assertIn("(3) 设棱台 $DEF - ABC$ 的体积为 $V$", self.transcript)
        self.assertIn("(1) 若 $C$ 的方程为", self.transcript)
        self.assertIn("(2) 若 $C$ 的方程为", self.transcript)
        self.assertIn("(3) 请选定一条除椭圆外的二次曲线 $C$", self.transcript)

    def test_high_risk_formulas_and_disputed_wording_match_source(self):
        expected = (
            r"\tan\left(\alpha + \dfrac{\pi}{4}\right)",
            r"x = -1",
            r"A \cap B = \{2\}",
            r"q = -\dfrac{1}{2}",
            r"x \in [0, 5]",
            r"A(1, -2)",
            r"(x + 1)^{10}",
            r"x = k\pi + (-1)^k",
            r"(1 + \mathrm{i})z_1 = -1 + 5\mathrm{i}",
            r"z_2 = a - 2 - \mathrm{i}",
            r"|z_1 - \overline{z_2}| < |z_1|",
            r"8\text{ cm}^2",
            r"f(x) = \sqrt{2 - \dfrac{x + 3}{x + 1}}",
            r"g(x) = \lg[(x - a - 1)(2a - x)]",
            r"B \subseteq A",
            r"f(x) = f_1(x) + f_2(x)",
            r"DEF - ABC",
            r"\dfrac{x^2}{100} + \dfrac{y^2}{25} = 1",
            r"P_1(3, 0)",
            r"S_3 = 255",
            r"\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1",
        )
        for formula in expected:
            self.assertIn(formula, self.transcript)

    def test_all_three_source_figures_are_registered_without_raster_embedding(self):
        figures = (
            "f2004_shanghai_science_q05_function_graph.tex",
            "f2004_shanghai_science_q18_frame_geometry.tex",
            "f2004_shanghai_science_q21_pyramid_frustum.tex",
        )
        paper = next(item for item in self.manifest["papers"] if item["paper_id"] == PAPER_ID)
        registered_figures = {fig["path"] for fig in paper["figure_files"]}
        for fig in figures:
            fig_path = PAPER_DIR / "figures" / fig
            self.assertTrue(fig_path.is_file(), f"figure file {fig} must exist")
            content = fig_path.read_text(encoding="utf-8")
            self.assertIn("\\begin{tikzpicture}", content)
            self.assertNotIn("\\includegraphics", content)
            self.assertIn(fig, self.transcript)
            self.assertIn(f"2004_上海卷_理科/figures/{fig}", registered_figures)

        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")

    def test_provenance_and_receipts_reflect_unresolved_blockers(self):
        prov_path = PAPER_DIR / "provenance.json"
        self.assertTrue(prov_path.is_file())
        prov = json.loads(prov_path.read_text(encoding="utf-8"))
        self.assertEqual(prov["paper_id"], PAPER_ID)
        questions = {q["question_order"]: q for q in prov["questions"]}
        self.assertEqual(set(questions), set(range(1, 23)))

        # Q19 must be U grade with ISSUE-1386
        q19 = questions[19]
        self.assertEqual(q19["answer_evidence"]["grade"], "U")
        self.assertEqual(q19["conflict_status"], "none")
        self.assertIn("ISSUE-1386", q19["issue_ids"])

        # Q22 must be U grade with ISSUE-1387
        q22 = questions[22]
        self.assertEqual(q22["answer_evidence"]["grade"], "U")
        self.assertEqual(q22["conflict_status"], "none")
        self.assertIn("ISSUE-1387", q22["issue_ids"])

        # Check receipts exist and reflect final states
        build_receipt = json.loads((PAPER_DIR / "receipts/build.json").read_text(encoding="utf-8"))
        self.assertEqual(build_receipt["status"], "succeeded")
        self.assertEqual(len(build_receipt["editions"]), 4)

        review_receipt = json.loads((PAPER_DIR / "receipts/review.json").read_text(encoding="utf-8"))
        self.assertEqual(review_receipt["status"], "passed")
        self.assertEqual(review_receipt["batch_id"], "phase4-b46")

        # 检查生成物当前性
        artifacts_state = provenance.default_artifacts_state(ROOT, self.manifest, PAPER_ID)
        self.assertEqual(artifacts_state, "current")

        # 检查四版 TeX 入口文件与简答文件完整性
        for edition_tex in ("试题版.tex", "解析版.tex", "简答版.tex", "印刷版.tex"):
            self.assertTrue((PAPER_DIR / edition_tex).is_file(), f"{edition_tex} 必须存在")

        answers_short = (PAPER_DIR / "answers_short.tex").read_text(encoding="utf-8")
        for num in list(range(1, 13)) + list(range(17, 23)):
            self.assertIn(f"\\item[\\textbf{{{num}.}}]", answers_short)
        for num in range(13, 17):
            self.assertIn(f"& {num}", answers_short)
        self.assertIn("& B & C & A & B", answers_short)

        # 检查 index.json 投影一致性
        idx_paper = next(p for p in self.index_doc["papers"] if p.get("dir") == "2004_上海卷_理科")
        self.assertEqual(idx_paper["id"], PAPER_ID)
        self.assertEqual(idx_paper["questions"], 22)
        self.assertEqual(len(idx_paper["figures"]), 3)
        self.assertEqual(idx_paper["structure"]["填空题"], [1, 12])
        self.assertEqual(idx_paper["structure"]["选择题"], [13, 16])
        self.assertEqual(idx_paper["structure"]["解答题"], [17, 22])


if __name__ == "__main__":
    unittest.main()
