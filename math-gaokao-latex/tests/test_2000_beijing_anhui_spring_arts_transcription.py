import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2000/2000_数学真题_春季北京安徽文_试题.md"
INVENTORY = ROOT / "2000/2000_数学真题_春季北京安徽文_图表清单.md"
ANSWERS = ROOT / "2000/2000_数学真题_春季北京安徽文_答案要点.md"
SOLUTIONS = ROOT / "2000/2000_数学真题_春季北京安徽文_解析正文.md"
FIGURES = ROOT / "2000/figures"
SOURCE_ID = "src-6d9f6ee269b4dd80d69001f2f4399956b5d037bfbf1d383a78bfdb281c440e6b"
SOURCE_SHA256 = "b9552b8354735296f6ea1ed051085e094e4af0c14ff97ada2dbd4e579b14287f"
SOURCE_PATH = "春季高考/2000/2000春季北京,安徽文.pdf"
FIGURE_FILES = {
    14: "gaokao_2000_spring_beijing_anhui_arts_q14_cubic.tex",
    21: "gaokao_2000_spring_beijing_anhui_arts_q21_folded_trapezoid.tex",
    23: "gaokao_2000_spring_beijing_anhui_arts_q23_parabola.tex",
}


class BeijingAnhuiSpring2000ArtsTranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        cls.inventory = INVENTORY.read_text(encoding="utf-8")

    def test_fixed_source_identity_and_registered_binding(self):
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(item for item in manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], SOURCE_PATH)
        self.assertEqual(source["source_state"], "ready")
        # 草稿中的 paper_id:null 是转录阶段快照；当前来源已正式绑定本批项目。
        self.assertEqual(source["paper_id"], "gk-2000-spring-jingwan-arts")
        self.assertEqual(source["paper_relation"], "canonical")
        paper = next(p for p in manifest["papers"] if p["paper_id"] == source["paper_id"])
        self.assertIn(SOURCE_ID, paper["source_ids"])
        for value in (SOURCE_ID, SOURCE_SHA256, "paper_id: null", "official_answer: null", "出版物/版次未知"):
            self.assertIn(value, self.transcript)
        self.assertIn("末张 `arts/sxws09.gif` 含 Q23、Q24 解题内容", self.inventory)
        self.assertIn("未据此转录题面或生成答案", self.inventory)

    def test_question_sequence_sections_and_math_delimiters(self):
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 25)))
        self.assertEqual(self.transcript.count("## 一、选择题"), 1)
        self.assertEqual(self.transcript.count("## 二、填空题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertEqual(self.transcript.count("$") % 2, 0)
        self.assertIn("（1）若二面角", self.transcript)
        self.assertIn("（2）若二面角", self.transcript)
        self.assertIn("（1）写出本年度", self.transcript)
        self.assertIn("（2）设 $k=0.2a$", self.transcript)

    def test_track_specific_items_and_high_risk_formulas_are_present(self):
        for text in (
            r"z_1=3+i$，$z_2=1-i",
            r"\overline{M}\cap\overline{N}",
            r"\dfrac{x^2}{b^2}-\dfrac{y^2}{a^2}=1",
            r"x^2y+xy^2=1",
            r"\dfrac56\pi",
            r"\sin\alpha+\sin\beta<\sqrt2",
            r"a_1+a_2+a_3+\cdots+a_{101}=0",
            r"\cos\left(\dfrac{2\pi}{3}x+\dfrac{\pi}{4}\right)",
            r"\left(\sqrt{x}-\dfrac{1}{\sqrt[3]{x}}\right)^{10}",
            r"(\lg a)x^2+2x+4\lg a",
            r"\frac{a^2-b^2}{c^2}=\frac{\sin(A-B)}{\sin C}",
            r"y^2=4px",
            "电价为 $0.8$ 元/kW·h",
        ):
            with self.subTest(text=text):
                self.assertIn(text, self.transcript)
        self.assertIn("函数 $y=\\sin x+\\cos x+2$", self.transcript)
        self.assertNotIn("（10）已知", self.transcript)

    def test_figure_inventory_links_match_all_visible_math_figures(self):
        for question, filename in FIGURE_FILES.items():
            with self.subTest(question=question):
                path = FIGURES / filename
                self.assertTrue(path.is_file())
                self.assertIn(f"figures/{filename}", self.transcript)
                self.assertIn(f"| {question} |", self.inventory)
                self.assertIn(filename, self.inventory)
                source = path.read_text(encoding="utf-8")
                self.assertEqual(source.count(r"\begin{tikzpicture}"), 1)
                self.assertEqual(source.count(r"\end{tikzpicture}"), 1)
                self.assertNotIn(r"\includegraphics", source)
                self.assertNotIn(".gif", source.lower())

        cubic = (FIGURES / FIGURE_FILES[14]).read_text(encoding="utf-8")
        for label in ("$x$", "$y$", "$O$", "$1$", "$2$"):
            self.assertIn(label, cubic)
        self.assertIn("not metrically exact", cubic)
        fold = (FIGURES / FIGURE_FILES[21]).read_text(encoding="utf-8")
        for label in ("$A$", "$B$", "$C$", "$D$", "$D'$", "图一", "图二", "图三"):
            self.assertIn(label, fold)
        first_figure = {
            label: tuple(float(value) for value in match.groups())
            for label in "ABCD"
            for match in [re.search(rf"\\coordinate \({label}1\) at \(([-0-9.]+),([-0-9.]+)\)", fold)]
            if match
        }
        self.assertEqual(set(first_figure), set("ABCD"))
        distance = lambda p, q: math.hypot(p[0] - q[0], p[1] - q[1])
        self.assertTrue(math.isclose(distance(first_figure["A"], first_figure["D"]), 1))
        self.assertTrue(math.isclose(distance(first_figure["D"], first_figure["C"]), 1))
        self.assertTrue(math.isclose(distance(first_figure["A"], first_figure["B"]), 2))
        self.assertIn("review-needed", self.inventory)
        parabola = (FIGURES / FIGURE_FILES[23]).read_text(encoding="utf-8")
        for label in ("$O$", "$A$", "$B$", "$M$", "$x$", "$y$"):
            self.assertIn(label, parabola)
        self.assertIn(r"$OA\perp OB$", self.transcript)
        self.assertIn(r"$OM\perp AB$", self.transcript)

    def test_transcript_contains_no_raster_figure_links(self):
        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")

    def test_independent_answer_and_solution_drafts_cover_all_questions(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        for document in (answers, solutions):
            self.assertIn(f"source_id: {SOURCE_ID}", document)
            self.assertIn(f"source_sha256: {SOURCE_SHA256}", document)
            self.assertIn("official_answer: null", document)
            self.assertIn("solution_status: draft-independent-solutions-pending-cross-check", document)
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．\*\*", solutions, re.M)]
        self.assertEqual(numbers, list(range(1, 25)))
        self.assertIn("| 答案 | D | A | C | B | C | B | B | B | D | A | C | D | C | A |", answers)
        self.assertIn("仅（B）关于 $x=y$ 对称", answers)
        self.assertIn("若允许$a=b$", answers)
        self.assertNotIn("A、B 都关于", solutions)
        self.assertNotIn("官方答案", solutions.split("## 一、选择题", 1)[1])
        self.assertIn("**19．** 令$t=\\lg a$", solutions)
        self.assertIn("**20．** 由正弦定理", solutions)
        self.assertIn("**21．** 取$a=1$作长度单位", solutions)
        self.assertIn("二面角$\\beta-BC-\\gamma=45^\\circ$", solutions)
        self.assertIn("**24．** (1) 降价后新增用电量", solutions)
        self.assertNotIn("f_1", solutions)

    @unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdftoppm"), "latexmk and Poppler are required")
    def test_all_new_tikz_sources_compile_and_render(self):
        work_root = ROOT / ".work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2000-beijing-anhui-arts-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            inputs = "\n\\newpage\n".join(
                r"\input{" + (FIGURES / filename).as_posix() + "}"
                for filename in FIGURE_FILES.values()
            )
            (build_dir / "figures.tex").write_text(
                "\\documentclass{article}\n"
                "\\usepackage[margin=1.5cm]{geometry}\n"
                "\\usepackage{tikz}\n"
                "\\usepackage{xeCJK}\n"
                "\\setCJKmainfont{Songti SC}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                + inputs
                + "\n\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figures.tex"],
                cwd=build_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pdf = build_dir / "figures.pdf"
            self.assertTrue(pdf.is_file())
            subprocess.run(
                ["pdftoppm", "-png", "-r", "120", str(pdf), str(build_dir / "figure")],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=120,
            )
            pages = sorted(build_dir.glob("figure-*.png"))
            self.assertEqual(len(pages), len(FIGURE_FILES))
            self.assertTrue(all(page.stat().st_size > 1000 for page in pages))
            if os.environ.get("KEEP_2000_BEIJING_ANHUI_ARTS_FIGURES") == "1":
                review_dir = work_root / "review-2000-beijing-anhui-arts-figures"
                review_dir.mkdir(exist_ok=True)
                for page in pages:
                    shutil.copy2(page, review_dir / page.name)


if __name__ == "__main__":
    unittest.main()
