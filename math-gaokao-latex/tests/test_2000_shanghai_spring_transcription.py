import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2000/2000_数学真题_春季上海_试题.md"


class ShanghaiSpring2000TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "math-gaokao-latex/source-manifest.json").read_text(encoding="utf-8"))

    def test_fixed_source_identity_and_canonical_binding_are_explicit(self):
        self.assertIn("src-2980f0ba5ee7c2ceec0fb5ea733769661ddc2a0012bd727f326ad93cd15a2bc0", self.transcript)
        self.assertIn("f58f3b980fef4e1b74955a9e37bbbf751056d4d3c9a2215d77b489fd14e5a954", self.transcript)
        paper_id = "gk-2000-spring-shanghai"
        source_id = "src-2980f0ba5ee7c2ceec0fb5ea733769661ddc2a0012bd727f326ad93cd15a2bc0"
        paper = next(row for row in self.manifest["papers"] if row["paper_id"] == paper_id)
        source = next(row for row in self.manifest["sources"] if row["source_id"] == source_id)
        self.assertEqual(paper["source_ids"], [source_id])
        self.assertEqual(source["paper_id"], paper_id)
        self.assertEqual(source["paper_relation"], "canonical")
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["artifact"]["sha256"], "f58f3b980fef4e1b74955a9e37bbbf751056d4d3c9a2215d77b489fd14e5a954")
        self.assertEqual(source["artifact"]["page_count"], 9)
        self.assertEqual(ROOT / paper["source_files"]["questions"], TRANSCRIPT)
        self.assertRegex(self.transcript, rf"(?m)^paper_id: {paper_id}$")
        self.assertEqual(paper["index_metadata"]["pages_q"], [1, 5])
        self.assertEqual(paper["index_metadata"]["pages_s"], [5, 9])
        self.assertIn("题面跨 PDF 第 1–5 页", self.transcript)
        self.assertIn("印刷页码 182–186", self.transcript)
        self.assertIn("第 5 页续 Q22 并起附录", self.transcript)
        self.assertIn("出版者、出版物、版次、来源链及官方身份未核", self.transcript)
        self.assertIn("不据此认定为官方答案", self.transcript)
        self.assertIn("本库官方答案状态仍为 null", self.transcript)

    def test_question_numbers_sections_and_points_are_complete(self):
        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("$") % 2, 0)
        self.assertEqual(self.transcript.count("## 一、填空题"), 1)
        self.assertEqual(self.transcript.count("## 二、选择题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertIn("满分 48 分，共 12 题", self.transcript)
        self.assertIn("满分 16 分，共 4 题", self.transcript)
        self.assertIn("满分 86 分，共 6 题", self.transcript)
        self.assertIn("第 1 小题满分 4 分，第 2 小题满分 6 分，第 3 小题满分 8 分", self.transcript)
        self.assertIn("每小题满分均为 6 分", self.transcript)

    def test_independently_reviewed_high_risk_transcription_details(self):
        for text in (
            r"\pi-\operatorname{arctg}\dfrac{1}{2}",
            "其中 $A$、$B$ 两件产品",
            "非空集合 $P$、$Q$",
            r"y=\cos^2 ax-\sin^2 ax",
            "在甲乙两家家电商场均有销售",
            r"\frac{a_{m+1}+a_{m+2}+\cdots+a_{2m}}{m+1}\le -160b_2",
            r"\overrightarrow{AB}=(2,-1,-4)",
            r"\frac{(y+1)^2}{16}+\frac{(x-1)^2}{12}=1",
        ):
            self.assertIn(text, self.transcript)
        self.assertIn("图像不经过", self.transcript)
        self.assertIn("射线 $OA$ 于 $Q$", self.transcript)

    def test_registered_diagrams_are_not_silently_dropped_or_replaced_with_rasters(self):
        self.assertIn("第 8 题（PDF 第 1 页）", self.transcript)
        self.assertIn("第 17 题（PDF 第 3 页）", self.transcript)
        self.assertIn("第 22 题（PDF 第 5 页，印刷页 186）", self.transcript)
        self.assertIn("本阶段将图稿归入正式项目目录", self.transcript)
        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")


if __name__ == "__main__":
    unittest.main()
