"""1985 广东理科版式回归：图中标签与附加题分页。"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT.parent.parent.parent
PAPER_ID = "gk-1985-regular-guangdong-science"
PAPER_DIR = PROJECT / "1985_广东卷_理工农医类"
QUESTION_SOURCE = REPOSITORY_ROOT / "1985/1985_数学真题_广东理工农医类_试题.md"
FIGURE_SOURCE = PAPER_DIR / "figures/f1985_guangdong_science_v1_q1_graphs.tex"

sys.path.insert(0, str(PROJECT / "tools"))

import build_projects
import generate_projects


class GuangdongScience1985LayoutSourceTests(unittest.TestCase):
    def test_q1_coordinate_labels_use_open_quadrants(self):
        figure = FIGURE_SOURCE.read_text(encoding="utf-8")
        points = re.findall(
            r"\\fill \(([^)]*)\) circle \(1pt\) node\[([^]]+)\] \{\$\(([^)]*)\)\$\};",
            figure,
        )
        self.assertEqual(
            [
                ("0,1", "above left", "0,1"),
                ("1,1", "below left", "1,1"),
                ("1,0", "above right", "1,0"),
                ("1,0", "above left", "1,0"),
                ("0,1", "below left", "0,1"),
            ],
            points,
        )

    def test_q35_local_needspace_directive_is_emitted_between_question_blocks(self):
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        paper = next(item for item in manifest["papers"] if item["paper_id"] == PAPER_ID)
        sources = generate_projects.paper_sources(paper)
        generated = generate_projects.generate_project(REPOSITORY_ROOT, sources)
        questions_target = "math-gaokao-latex/%s/questions.tex" % sources.project_dir
        questions_tex = generated.targets[questions_target].decode("utf-8")

        self.assertNotIn("question-needspace:", questions_tex)
        q34_end = questions_tex.index("\\end{question}", questions_tex.index("\\gktiwithlabel{34}"))
        directive = r"\renewenvironment{question}{\Needspace{0.08\textheight}}{}"
        directive_index = questions_tex.index(directive)
        q35_start = questions_tex.index("\\begin{question}", q34_end + len("\\end{question}"))
        self.assertLess(q34_end, directive_index)
        self.assertLess(directive_index, q35_start)
        self.assertIn("\\gktiwithlabel{35}", questions_tex[q35_start:])


@unittest.skipUnless(
    all(shutil.which(tool) for tool in ("latexmk", "xelatex", "pdfinfo", "pdftotext")),
    "latexmk/xelatex/Poppler 不齐，无法运行真实 PDF 回归",
)
class GuangdongScience1985PaginationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        paper = next(item for item in manifest["papers"] if item["paper_id"] == PAPER_ID)
        sources = generate_projects.paper_sources(paper)
        generated = generate_projects.generate_project(REPOSITORY_ROOT, sources)

        cls.temporary = tempfile.TemporaryDirectory(prefix="gk1985-science-layout-")
        root = Path(cls.temporary.name)
        project_copy = root / "docs" / "exams" / "math-gaokao-latex"
        project_copy.mkdir(parents=True)
        shutil.copytree(PROJECT / "common", project_copy / "common")
        shutil.copytree(
            PROJECT / sources.project_dir,
            project_copy / sources.project_dir,
            ignore=shutil.ignore_patterns("build", "receipts", ".work"),
        )
        questions_target = "math-gaokao-latex/%s/questions.tex" % sources.project_dir
        (project_copy / sources.project_dir / "questions.tex").write_bytes(
            generated.targets[questions_target]
        )

        toolchain = build_projects.resolve_toolchain()
        cls.result = build_projects.build_target(root, sources.project_dir, "试题版", toolchain)
        pdf = root / cls.result["record"]["pdf"]["path"]
        pdftotext = next(
            tool["path"] for tool in toolchain["tools"] if tool["name"] == "pdftotext"
        )
        cls.pages = [
            re.sub(r"\s+", "", page)
            for page in subprocess.run(
                [pdftotext, "-layout", str(pdf), "-"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.split("\f")
            if page.strip()
        ]

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_bonus_question_shares_a_page_with_q34(self):
        q34_pages = [
            index for index, page in enumerate(self.pages)
            if "椭圆I和抛物线II的交点与坐标原点的距离" in page
        ]
        q35_pages = [
            index for index, page in enumerate(self.pages)
            if "不同实根的个数不大于3" in page
        ]
        self.assertEqual(1, len(q34_pages))
        self.assertEqual(1, len(q35_pages))
        self.assertEqual(q34_pages[0], q35_pages[0])


if __name__ == "__main__":
    unittest.main()
