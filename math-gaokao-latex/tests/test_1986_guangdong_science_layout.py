"""1986 广东理科试题版分页回归。"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT.parent
PAPER_ID = "gk-1986-regular-guangdong-science"
sys.path.insert(0, str(PROJECT / "tools"))

import build_projects
import generate_projects


@unittest.skipUnless(
    all(shutil.which(tool) for tool in ("latexmk", "xelatex", "pdfinfo", "pdftotext", "pdftoppm")),
    "latexmk/xelatex/Poppler 不齐，无法运行真实 PDF 回归",
)
class GuangdongScience1986LayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        paper = next(p for p in manifest["papers"] if p["paper_id"] == PAPER_ID)
        sources = generate_projects.paper_sources(paper)
        generated = generate_projects.generate_project(REPOSITORY_ROOT, sources)

        cls.temporary = tempfile.TemporaryDirectory(prefix="gk1986-science-layout-")
        root = Path(cls.temporary.name)
        project_copy = root / "math-gaokao-latex"
        project_copy.mkdir(parents=True)
        shutil.copytree(PROJECT / "common", project_copy / "common")
        shutil.copytree(
            PROJECT / sources.project_dir,
            project_copy / sources.project_dir,
            ignore=shutil.ignore_patterns("build", "receipts", ".work"),
        )
        questions_target = (
            "math-gaokao-latex/%s/questions.tex" % sources.project_dir
        )
        (project_copy / sources.project_dir / "questions.tex").write_bytes(
            generated.targets[questions_target]
        )

        toolchain = build_projects.resolve_toolchain()
        cls.result = build_projects.build_target(
            root, sources.project_dir, "试题版", toolchain
        )
        pdf = root / cls.result["record"]["pdf"]["path"]
        pdftotext = next(
            tool["path"] for tool in toolchain["tools"]
            if tool["name"] == "pdftotext"
        )
        cls.extracted = subprocess.run(
            [pdftotext, "-layout", str(pdf), "-"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

        cls.print_result = build_projects.build_target(
            root, sources.project_dir, "印刷版", toolchain
        )
        print_pdf = root / cls.print_result["record"]["pdf"]["path"]
        cls.print_extracted = subprocess.run(
            [pdftotext, "-layout", str(print_pdf), "-"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_question_paper_does_not_disclose_solutions_in_editorial_notes(self):
        self.assertEqual([], self.result["record"]["problems"])
        compact = re.sub(r"\s+", "", self.extracted)
        self.assertTrue("答案表对应" not in compact, "question PDF leaks answer-key mapping")
        self.assertTrue("按题意解释为乘法" not in compact, "question PDF guesses the missing operator")
        self.assertTrue("具体符号待核" in compact, "question PDF omits uncertainty status")

    def test_each_unreadable_source_operator_is_attributed_to_its_question(self):
        compact = re.sub(r"\s+", "", self.extracted)
        for marker in ("第2题（2）", "第2题（9）", "第5题（2）"):
            with self.subTest(marker=marker):
                self.assertTrue(marker in compact, f"missing uncertainty note: {marker}")

    def test_question_18_retains_source_note_that_interval_is_decreasing(self):
        compact = re.sub(r"\s+", "", self.extracted)
        self.assertIn(
            "的单调下降区间（即在该区间内函数为减函数）是",
            compact,
        )

    def test_last_question_page_keeps_all_of_question_five_with_question_six(self):
        question_six_pages = [
            page for page in self.extracted.split("\f")
            if "椭圆 C 的直角坐标方程" in page and "试确定 m 的取值范围" in page
        ]
        self.assertEqual(1, len(question_six_pages))
        final_question_page = question_six_pages[0]
        compact = re.sub(r"\s+", "", final_question_page)
        self.assertTrue("试用an−1" in compact, "question 5 part 1 moved off the final page")
        self.assertTrue("用数学归纳法证明" in compact, "question 5 part 2 moved off the final page")
        self.assertTrue("（3）求" in compact, "question 5 part 3 moved off the final page")

    def test_print_version_keeps_question_nine_options_on_one_page(self):
        self.assertEqual([], self.print_result["record"]["problems"])
        pages = [
            re.sub(r"\s+", "", page)
            for page in self.print_extracted.split("\f")
            if page.strip()
        ]
        question_nine = next(
            page for page in pages
            if "（9）要排一张有5个独唱节目" in page
        )
        question_nine_block = question_nine.split("（10）")[0]
        for option in ("（D）P55□P83", "（E）P85□P83"):
            with self.subTest(option=option):
                self.assertTrue(
                    option in question_nine_block,
                    f"print version splits question 9 {option} across pages",
                )


if __name__ == "__main__":
    unittest.main()
