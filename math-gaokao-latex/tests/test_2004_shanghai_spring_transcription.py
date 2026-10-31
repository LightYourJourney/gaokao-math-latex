import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季上海_试题.md"
FIGURES = ROOT / "2004/2004_数学真题_春季上海_图表清单.md"
Q11_FIGURE = PROJECT / "2004_春季上海卷/figures/gaokao_2004_shanghai_spring_q11_pascal.tex"
Q6_FIGURE = PROJECT / "2004_春季上海卷/figures/gaokao_2004_shanghai_spring_q06_pyramid.tex"
Q8_FIGURE = PROJECT / "2004_春季上海卷/figures/gaokao_2004_shanghai_spring_q08_patterns.tex"
Q20_FIGURE = PROJECT / "2004_春季上海卷/figures/gaokao_2004_shanghai_spring_q20_oblique_prism.tex"
SOURCE_ID = "src-eda3090af4489c2848005279f9f1f65a561d4fa54daf91ccd574cfbff213be4f"
SOURCE_SHA256 = "e09d135e7814d1d5dd658ac51829a170edae1267b408f30a4edfa44d2312ca8a"


class ShanghaiSpring2004TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        cls.figures = FIGURES.read_text(encoding="utf-8")
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def test_fixed_source_identity_matches_internal_binding(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], "春季高考/2004/2004春季上海.pdf")
        self.assertEqual(source["paper_id"], "gk-2004-spring-shanghai")
        self.assertEqual(source["paper_relation"], "canonical")
        paper = next(item for item in self.manifest["papers"] if item["paper_id"] == source["paper_id"])
        self.assertEqual(paper["production_state"], "blocked")
        self.assertTrue({"ISSUE-1264", "ISSUE-1265", "ISSUE-1266"}.issubset(paper["issue_ids"]))
        self.assertIn(SOURCE_ID, self.transcript)
        self.assertIn(SOURCE_SHA256, self.transcript)
        self.assertIn("内部卷件标识绑定", self.transcript)
        self.assertIn("不代表官方身份认证", self.transcript)

    def test_provenance_preserves_pending_interpretations(self):
        path = PROJECT / "2004_春季上海卷/provenance.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        questions = {item["question_order"]: item for item in document["questions"]}
        self.assertEqual(set(questions), set(range(1, 23)))
        self.assertEqual(questions[14]["answer_evidence"]["grade"], "U")
        self.assertEqual(questions[14]["conflict_status"], "unresolved")
        self.assertEqual(set(questions[14]["issue_ids"]), {"ISSUE-1264", "ISSUE-1266"})
        self.assertEqual(questions[18]["answer_evidence"]["grade"], "U")
        self.assertEqual(questions[18]["conflict_status"], "resolved")
        self.assertIn("ISSUE-1265", questions[18]["issue_ids"])
        self.assertIn("早期第二盲解将 x 误作 p", questions[18]["answer_evidence"]["evidence"])
        self.assertEqual(questions[19]["source_pages"], [1])
        self.assertEqual(questions[20]["source_pages"], [2])

    def test_question_numbers_sections_and_math_delimiters_are_complete(self):
        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("## 一、填空题"), 1)
        self.assertEqual(self.transcript.count("## 二、选择题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertEqual(self.transcript.count("$") % 2, 0)

    def test_source_wording_and_high_risk_formulas_are_preserved(self):
        for expected in (
            r"f(x)=\log_3\left(\dfrac{4}{x}+2\right)",
            r"(\sqrt{a_n},\sqrt{a_{n-1}})",
            r"4(x+3)^2+9y^2=36",
            r"\overrightarrow{AB}-\overrightarrow{AC}=\overrightarrow{BC}",
            r"\dfrac{2x+1}{x+2}<0",
            r"10^{f(n)}\cdot\left(\dfrac{4}{5}\right)^{g(n)}<4",
            r"\dfrac{x^2}{a^2}-y^2=1",
        ):
            self.assertIn(expected, self.transcript)
        self.assertIn("实数 $p$ 满足不等式", self.transcript)
        self.assertIn("未将 $x$ 擅改为 $p$", self.transcript)

    def test_all_source_figures_are_registered_without_raster_embedding(self):
        for question in ("第 6 题", "第 8 题", "第 11 题", "第 20 题"):
            self.assertIn(question, self.figures)
            self.assertIn(question, self.transcript)
        self.assertIn("1,3,7,13,21", self.figures)
        self.assertIn("第 0 行", self.figures)
        self.assertIn("1,5,10,10,5,1", self.figures)
        reviewed_statuses = re.findall(r"^- 状态：独立图像终核通过，.*$", self.figures, re.M)
        self.assertEqual(len(reviewed_statuses), 4)
        self.assertNotIn("待独立", self.figures)
        self.assertIn("$AB$ 为实线", self.figures)
        self.assertIn("$AC$ 与 $AE$ 为虚线", self.figures)
        self.assertTrue(Q11_FIGURE.is_file())
        self.assertTrue(Q6_FIGURE.is_file())
        self.assertTrue(Q8_FIGURE.is_file())
        self.assertTrue(Q20_FIGURE.is_file())
        self.assertIn("figures/gaokao_2004_shanghai_spring_q06_pyramid.tex", self.transcript)
        self.assertIn("figures/gaokao_2004_shanghai_spring_q08_patterns.tex", self.transcript)
        self.assertIn("figures/gaokao_2004_shanghai_spring_q20_oblique_prism.tex", self.transcript)
        self.assertIn("figures/gaokao_2004_shanghai_spring_q11_pascal.tex", self.transcript)
        q11_source = Q11_FIGURE.read_text(encoding="utf-8")
        self.assertEqual(q11_source.count(r"\cdots"), 4)
        self.assertNotIn(r"\vdots", q11_source)
        self.assertIn("第 \\r 行", q11_source)
        self.assertIn(r"\foreach \r in {0,...,5}", q11_source)
        self.assertNotIn(r"\includegraphics", q11_source)
        q6_source = Q6_FIGURE.read_text(encoding="utf-8")
        self.assertIn(r"\draw[dashed] (A)--(C) (A)--(E);", q6_source)
        self.assertIn(r"\draw (A)--(B)--(C);", q6_source)
        self.assertNotIn(r"\includegraphics", q6_source)
        q8_source = Q8_FIGURE.read_text(encoding="utf-8")
        self.assertEqual(q8_source.count(r"\draw[fill=white]"), 1)
        points = re.findall(r"(-?\d+(?:\.\d+)?)/(-?\d+(?:\.\d+)?)", q8_source)
        self.assertEqual(len(points), 45)
        self.assertEqual(len(set(points)), 45)
        self.assertNotIn(r"\includegraphics", q8_source)
        q20_source = Q20_FIGURE.read_text(encoding="utf-8")
        for label in ("A", "B", "C", "A1", "B1", "C1", "P", "M", "N"):
            self.assertIn(f"({label})", q20_source)
        self.assertIn(r"\coordinate (P)  at (-0.48,1.54);", q20_source)
        self.assertIn(r"\draw[dashed] (A)--(A1) (B1)--(A1)--(C1);", q20_source)
        self.assertNotIn(r"\includegraphics", q20_source)
        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")

    @unittest.skipUnless(shutil.which("latexmk"), "latexmk is required for the vector-figure smoke build")
    def test_pascal_triangle_figure_compiles_and_renders(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2004-shanghai-q11-", dir=work_root) as temp:
            build_dir = Path(temp)
            (build_dir / "figure.tex").write_text(
                "\\documentclass{ctexart}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                "\\input{" + str(Q11_FIGURE) + "}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figure.pdf"
            self.assertTrue(pdf.is_file())
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "120", str(pdf), str(build_dir / "figure")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            self.assertGreater((build_dir / "figure.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2004_SHANGHAI_Q11_REVIEW") == "1":
                review_dir = PROJECT / ".work/review-2004-shanghai-q11"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(build_dir / "figure.png", review_dir / "q11-pascal.png")

    @unittest.skipUnless(shutil.which("latexmk"), "latexmk is required for the vector-figure smoke build")
    def test_pyramid_figure_compiles_and_renders(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2004-shanghai-q06-", dir=work_root) as temp:
            build_dir = Path(temp)
            (build_dir / "figure.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                "\\input{" + str(Q6_FIGURE) + "}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figure.pdf"
            self.assertTrue(pdf.is_file())
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "120", str(pdf), str(build_dir / "figure")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            self.assertGreater((build_dir / "figure.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2004_SHANGHAI_Q06_REVIEW") == "1":
                review_dir = PROJECT / ".work/review-2004-shanghai-q06"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(build_dir / "figure.png", review_dir / "q06-pyramid.png")

    @unittest.skipUnless(shutil.which("latexmk"), "latexmk is required for the vector-figure smoke build")
    def test_point_pattern_figure_compiles_and_renders(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2004-shanghai-q08-", dir=work_root) as temp:
            build_dir = Path(temp)
            (build_dir / "figure.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                "\\input{" + str(Q8_FIGURE) + "}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figure.pdf"
            self.assertTrue(pdf.is_file())
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "160", str(pdf), str(build_dir / "figure")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            self.assertGreater((build_dir / "figure.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2004_SHANGHAI_Q08_REVIEW") == "1":
                review_dir = PROJECT / ".work/review-2004-shanghai-q08"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(build_dir / "figure.png", review_dir / "q08-patterns.png")

    @unittest.skipUnless(shutil.which("latexmk"), "latexmk is required for the vector-figure smoke build")
    def test_oblique_prism_figure_compiles_and_renders(self):
        work_root = PROJECT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2004-shanghai-q20-", dir=work_root) as temp:
            build_dir = Path(temp)
            (build_dir / "figure.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                "\\input{" + str(Q20_FIGURE) + "}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figure.pdf"
            self.assertTrue(pdf.is_file())
            subprocess.run(
                ["pdftoppm", "-singlefile", "-png", "-r", "160", str(pdf), str(build_dir / "figure")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            self.assertGreater((build_dir / "figure.png").stat().st_size, 1000)
            if os.environ.get("KEEP_2004_SHANGHAI_Q20_REVIEW") == "1":
                review_dir = PROJECT / ".work/review-2004-shanghai-q20"
                review_dir.mkdir(exist_ok=True)
                shutil.copy2(build_dir / "figure.png", review_dir / "q20-prism.png")


if __name__ == "__main__":
    unittest.main()
