import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "2003/2003_数学真题_春季上海_试题.md"
FIGURES = ROOT / "math-gaokao-latex/2003_春季上海卷/figures"
PROJECT_DIR = "2003_春季上海卷"
sys.path.insert(0, str(ROOT / "math-gaokao-latex/tools"))
from generate_projects import ProjectSources, generate_project, validate_project_result
EXPECTED = {
    18: "gaokao_2003_shanghai_spring_q18_sine.tex",
    19: "gaokao_2003_shanghai_spring_q19_prism.tex",
}


class ShanghaiSpring2003FigureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paper = PAPER.read_text(encoding="utf-8")

    def test_each_source_figure_is_linked_from_its_question(self):
        for question, filename in EXPECTED.items():
            with self.subTest(question=question):
                heading = re.search(rf"^\*\*{question}．.*?(?=^\*\*\d+．|\Z)", self.paper, re.M | re.S)
                self.assertIsNotNone(heading)
                self.assertIn(f"../math-gaokao-latex/{PROJECT_DIR}/figures/{filename}", heading.group())
                self.assertTrue((FIGURES / filename).is_file())

    def test_figures_are_vector_sources_and_keep_source_specific_features(self):
        for filename in EXPECTED.values():
            self.assertTrue((FIGURES / filename).is_file(), f"missing vector source {filename}")
        sources = {q: (FIGURES / name).read_text(encoding="utf-8") for q, name in EXPECTED.items()}
        for source in sources.values():
            self.assertEqual(source.count(r"\begin{tikzpicture}"), 1)
            self.assertEqual(source.count(r"\end{tikzpicture}"), 1)
            self.assertNotIn(r"\includegraphics", source)
        for landmark in ("2*sin", "-90", "630", r"\frac{3\pi}{2}", r"\frac{5\pi}{2}"):
            self.assertIn(landmark, sources[18])
        for label in ("A", "B", "C", "A_1", "B_1", "C_1"):
            self.assertIn(label, sources[19])
        for edge in ("(A)--(C)", "(B)--(C)", "(C)--(C1)", "(A1)--(C)"):
            self.assertIn(edge, sources[19])

    def test_official_project_generator_accepts_sources_and_figure_mapping(self):
        sources = ProjectSources(
            paper_id="gk-2003-spring-shanghai",
            project_dir=PROJECT_DIR,
            title="2003 年·春季上海卷",
            question_count=22,
            questions="2003/2003_数学真题_春季上海_试题.md",
            answer_key="2003/2003_数学真题_春季上海_答案要点.md",
            solution_body="2003/2003_数学真题_春季上海_解析正文.md",
            figures=tuple((f"{PROJECT_DIR}/figures/{name}", 2) for name in EXPECTED.values()),
        )
        result = generate_project(ROOT, sources)
        self.assertEqual(validate_project_result(sources, result), ())
        self.assertEqual(result.figure_occurrences, {
            f"{PROJECT_DIR}/figures/{name}": 2 for name in EXPECTED.values()
        })

    @unittest.skipUnless(shutil.which("latexmk") and all((FIGURES / name).is_file() for name in EXPECTED.values()), "latexmk and figure sources are required for vector figure smoke builds")
    def test_figures_compile_and_render(self):
        work_root = ROOT / "math-gaokao-latex/.work"
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="2003-shanghai-figures-", dir=work_root) as temp:
            build_dir = Path(temp)
            inputs = r"\input{" + str(FIGURES / EXPECTED[18]) + r"}" + "\n\\newpage\n" + r"\input{" + str(FIGURES / EXPECTED[19]) + r"}"
            (build_dir / "figures.tex").write_text(
                "\\documentclass{article}\n\\usepackage[margin=1.5cm]{geometry}\n\\usepackage{tikz}\n\\pagestyle{empty}\n\\begin{document}\n"
                + inputs + "\n\\end{document}\n", encoding="utf-8"
            )
            subprocess.run(
                ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figures.tex"],
                cwd=build_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, timeout=120,
            )
            prefix = build_dir / "figure"
            subprocess.run(
                ["pdftoppm", "-png", "-r", "120", str(build_dir / "figures.pdf"), str(prefix)],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120,
            )
            pages = sorted(build_dir.glob("figure-*.png"))
            self.assertEqual(len(pages), 2)
            self.assertTrue(all(page.stat().st_size > 1000 for page in pages))
            if os.environ.get("KEEP_2003_SHANGHAI_FIGURE_REVIEW") == "1":
                review_dir = work_root / "review-2003-shanghai-figures"
                review_dir.mkdir(exist_ok=True)
                for page in pages:
                    shutil.copy2(page, review_dir / page.name)


if __name__ == "__main__":
    unittest.main()
