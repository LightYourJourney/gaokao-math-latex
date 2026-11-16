import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2003/2003_数学真题_春季北京文_试题.md"
REVIEW = ROOT / "2003/2003_春季北京文科_来源校对.json"
FIGURE_INDEX = ROOT / "2003/2003_数学真题_春季北京文_图表清单.md"
SOURCE_MANIFEST = PROJECT / "source-manifest.json"
SOURCE_ID = "src-4ac986eba3d22fd3034252b57e1fed7e2b7b90eaaef7706499eb43fad52756e1"
PAPER_ID = "gk-2003-spring-beijing-arts"
SOURCE_SHA256 = "fbb6d54c9af88a7fc594be969b8e61c24bb37d98c05061cceaaf5d1be999c5c6"


class BeijingSpring2003ArtsTranscriptionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(TRANSCRIPT.is_file(), "fixed-source transcript draft is missing")
        self.assertTrue(REVIEW.is_file(), "source review record is missing")
        self.assertTrue(FIGURE_INDEX.is_file(), "figure inventory is missing")
        self.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        self.review = json.loads(REVIEW.read_text(encoding="utf-8"))
        self.figure_index = FIGURE_INDEX.read_text(encoding="utf-8")
        self.manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        self.paper = next(item for item in self.manifest["papers"] if item["paper_id"] == PAPER_ID)
        self.project_dir = PROJECT / self.paper["project_dir"]

    def test_source_record_and_transcript_remain_bound_to_fixed_canonical_input(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["paper_id"], PAPER_ID)
        self.assertEqual(source["paper_relation"], "canonical")
        self.assertEqual(self.paper["source_ids"], [SOURCE_ID])
        self.assertEqual(ROOT / self.paper["source_files"]["questions"], TRANSCRIPT)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertTrue(source["artifact"]["git_oid_verified"])

        self.assertEqual(self.review["source_id"], SOURCE_ID)
        self.assertEqual(self.review["paper_id"], PAPER_ID)
        self.assertEqual(self.review["transcription"]["path"], self.paper["source_files"]["questions"])
        self.assertEqual(self.review["source"]["git_blob_oid"], source["git_blob_oid"])
        self.assertEqual(self.review["source"]["sha256"], SOURCE_SHA256)
        self.assertIsNone(self.review["official_answer"])
        actual_transcript_hash = hashlib.sha256(TRANSCRIPT.read_bytes()).hexdigest()
        self.assertEqual(self.review["transcription"]["sha256"], actual_transcript_hash)
        self.assertEqual(self.review["source"]["source_authenticity"], "publisher-and-edition-unverified")
        frontmatter = self.transcript.split("---", 2)[1]
        self.assertRegex(frontmatter, rf"(?m)^paper_id: {re.escape(PAPER_ID)}$")
        self.assertRegex(frontmatter, r"(?m)^official_answer: null$")
        self.assertIn("内部 canonical 输入", frontmatter)
        self.assertIn("发布者/版次/来源链未核", frontmatter)
        self.assertIn("不认证其发布者、版次、来源链或官方身份", self.transcript)

    def test_all_22_questions_and_three_sections_are_transcribed_in_order(self):
        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("## 一、选择题"), 1)
        self.assertEqual(self.transcript.count("## 二、填空题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertEqual(self.review["transcription"]["question_numbers"], numbers)
        self.assertEqual(self.review["transcription"]["question_count"], 22)
        self.assertEqual(self.review["transcription"]["question_types"], {
            "single_choice": list(range(1, 13)),
            "fill_in": list(range(13, 17)),
            "written_response": list(range(17, 23)),
        })
        self.assertEqual(self.review["transcription"]["status"], "draft-transcribed-independently-reviewed")
        self.assertEqual(self.review["transcription"]["independent_review"], "passed")
        self.assertIn("Questions 1-22", self.review["transcription"]["independent_review_scope"])
        self.assertIn("ambiguous between I and L", self.review["transcription"]["independent_review_notes"])
        self.assertIn("题面复核状态: 独立盲核通过", self.transcript)
        self.assertIn("I/L", self.transcript)
        self.assertEqual(
            self.review["figures_and_tables"]["vector_reconstruction_status"],
            "draft-independently-reviewed",
        )
        self.assertIn("Q9, Q11, Q14, Q19, Q22", self.review["figures_and_tables"]["independent_review_scope"])
        self.assertIn("Q14", self.review["figures_and_tables"]["independent_review_notes"])
        self.assertEqual(self.transcript.count("$") % 2, 0)

    def test_high_risk_symbols_and_table_cells_match_the_fixed_scan(self):
        for source_detail in (
            r"$a>b$、$c>d$",
            r"\arg\dfrac{z_1}{z_2}",
            r"a^2x^2+b^2y^2=1",
            r"ax+by^2=0",
            r"abc\ne0",
            r"\triangle POF_2",
            r"\cos 2x",
            r"BD_1\parallel\text{平面 }C_1DE",
            r"距离的比为定值 $a$",
            r"$3000$ 元",
            r"\lim_{n\to\infty}(a_1+a_2+\cdots+a_n)",
        ):
            self.assertIn(source_detail, self.transcript, f"missing high-risk source detail: {source_detail}")
        self.assertIn(r"\log_2(x^2-x-2)>\log_2(2x-2)", self.transcript)
        self.assertIn(r"\underline{\qquad}", self.transcript)
        self.assertIn("PDF 第 1–2 页", self.transcript)
        self.assertIn("原卷印刷页码 121–122", self.transcript)

    def test_printed_title_and_q22_side_symbol_match_the_fixed_scan(self):
        self.assertIn("# 2003 普通高等学校春季招生考试（北京卷文）", self.transcript)
        self.assertNotIn("# 2003 年普通高等学校春季招生考试（北京卷文）", self.transcript)
        self.assertNotIn("## 数学试卷", self.transcript)
        self.assertIn("在边长为 $l$ 的等边", self.transcript)
        self.assertNotIn(r"边长为 $\ell$", self.transcript)

    def test_nontext_figures_have_linked_vector_sources_and_no_raster_substitutes(self):
        expected = {
            "q09-conic-options",
            "q11-folded-tetrahedron",
            "q14-cylinder-sphere",
            "q19-square-prism",
            "q22-tangent-circle-sequence",
        }
        self.assertTrue(expected.issubset(set(self.review["figures_and_tables"]["items"])))
        self.assertFalse(self.review["figures_and_tables"]["raster_source_committed"])
        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")
        figures = self.review["figures_and_tables"]["vector_assets"]
        self.assertEqual({figure["item"] for figure in figures}, expected)
        self.assertEqual(len(figures), len(expected))
        manifest_figures = {PROJECT / figure["path"] for figure in self.paper["figure_files"]}
        self.assertEqual(manifest_figures, {ROOT / figure["path"] for figure in figures})
        self.assertTrue(all(figure["expected_occurrences"] == 2 for figure in self.paper["figure_files"]))
        for figure in figures:
            file_path = ROOT / figure["path"]
            self.assertEqual(file_path.parent, self.project_dir / "figures")
            self.assertTrue(file_path.is_file(), figure["path"])
            contents = file_path.read_text(encoding="utf-8")
            self.assertIn(r"\begin{tikzpicture}", contents)
            self.assertIn(r"\end{tikzpicture}", contents)
            self.assertEqual(hashlib.sha256(file_path.read_bytes()).hexdigest(), figure["sha256"])
            self.assertIn(file_path.name, self.transcript)
            self.assertIn(file_path.name, self.figure_index)
            for document, contents in ((TRANSCRIPT, self.transcript), (FIGURE_INDEX, self.figure_index)):
                links = re.findall(r"\]\(([^)]+\.tex)\)", contents)
                matching_links = [link for link in links if Path(link).name == file_path.name]
                self.assertEqual(len(matching_links), 1, f"missing or duplicated figure link in {document}")
                self.assertEqual((document.parent / matching_links[0]).resolve(), file_path.resolve())

    def test_q11_vector_includes_the_two_segments_whose_angle_is_asked(self):
        figure = self.project_dir / "figures/gaokao_2003_beijing_arts_q11_folded_tetrahedron.tex"
        contents = figure.read_text(encoding="utf-8")
        self.assertIn(r"\draw (G)--(H) (J)--(I);", contents)

    def test_q19_vector_includes_hidden_edges_of_the_asked_tetrahedron(self):
        figure = self.project_dir / "figures/gaokao_2003_beijing_arts_q19_square_prism.tex"
        contents = figure.read_text(encoding="utf-8")
        self.assertRegex(contents, r"\\draw\[dashed\][^\n]*\(D\)--\(B\)")
        self.assertRegex(contents, r"\\draw\[dashed\][^\n]*\(D1\)--\(C\)")

    def test_q22_vector_includes_the_third_tangent_circle_visible_in_the_scan(self):
        figure = self.project_dir / "figures/gaokao_2003_beijing_arts_q22_tangent_circle_sequence.tex"
        contents = figure.read_text(encoding="utf-8")
        self.assertIn(r"\coordinate (Othree)", contents)
        self.assertIn(r"\draw (Othree) circle (", contents)
        self.assertIn(r"\fill (Othree) circle (", contents)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and pdftoppm are required")
    def test_all_vector_figures_compile_and_render_as_nonempty_pages(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        figures = self.review["figures_and_tables"]["vector_assets"]
        with tempfile.TemporaryDirectory(prefix="2003-beijing-arts-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            body = (r"\clearpage" + "\n").join(
                r"\input{" + str(ROOT / figure["path"]) + "}" for figure in figures
            )
            (build_dir / "figures.tex").write_text(
                "\n".join((
                    r"\documentclass[UTF8]{ctexart}",
                    r"\usepackage[margin=1.5cm]{geometry}",
                    r"\usepackage{tikz}",
                    r"\pagestyle{empty}",
                    r"\begin{document}", body, r"\end{document}",
                )) + "\n",
                encoding="utf-8",
            )
            try:
                subprocess.run(
                    ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figures.tex"],
                    cwd=build_dir, check=True, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, timeout=120,
                )
            except subprocess.CalledProcessError as exc:
                self.fail(f"latexmk rejected a source-vector figure:\n{exc.stdout[-4000:]}")
            subprocess.run(
                ["pdftoppm", "-png", "-r", "120", "figures.pdf", "figures"],
                cwd=build_dir, check=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            pages = sorted(build_dir.glob("figures-*.png"))
            self.assertEqual(len(pages), len(figures))
            self.assertTrue(all(page.stat().st_size > 1500 for page in pages))
            if os.environ.get("KEEP_2003_BEIJING_ARTS_FIGURES") == "1":
                for index, page in enumerate(pages, 1):
                    shutil.copy2(page, PROJECT / f".work/review-2003-beijing-arts-figures-{index}.png")


if __name__ == "__main__":
    unittest.main()
