import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER_DIR = PROJECT / "2017_上海春季卷"
FIGURE_DIR = PAPER_DIR / "figures"
TRANSCRIPT = ROOT / "2017/2017_数学真题_春季上海_试题.md"
COMBINED = ROOT / "2017/2017_数学真题_春季上海_含解析.md"
FIGURE_LIST = ROOT / "2017/2017_数学真题_春季上海_图表清单.md"
MANIFEST = PROJECT / "source-manifest.json"
PAPER_ID = "gk-2017-spring-shanghai"
FIGURES = {
    16: "2017_shanghai_spring_q16_octagon.tex",
    17: "2017_shanghai_spring_q17_prism.tex",
    19: "2017_shanghai_spring_q19_tangent_circles.tex",
}


class ShanghaiSpring2017FigureTests(unittest.TestCase):
    def test_each_canonical_markdown_explicitly_links_the_registered_tikz_source(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        paper = next(item for item in manifest["papers"] if item["paper_id"] == PAPER_ID)
        expected = [
            {
                "path": "2017_上海春季卷/figures/" + filename,
                "expected_occurrences": 2,
            }
            for filename in FIGURES.values()
        ]
        self.assertEqual(paper["figure_files"], expected)

        for source in (TRANSCRIPT, COMBINED):
            text = source.read_text(encoding="utf-8")
            for filename in FIGURES.values():
                target = "../math-gaokao-latex/2017_上海春季卷/figures/" + filename
                self.assertEqual(text.count("](" + target + ")"), 1, (source, filename))
            self.assertNotRegex(text, r"!\[[^\]]*\]\([^)]*\.(?:png|jpe?g)(?:\?[^)]*)?\)")

    def test_q16_is_a_regular_octagon_with_p_on_a6_a7_and_two_outgoing_vectors(self):
        source = (FIGURE_DIR / FIGURES[16]).read_text(encoding="utf-8")
        for vertex in range(1, 9):
            self.assertIn("(A%d)" % vertex, source)
            self.assertIn(r"\coordinate (A%d) at" % vertex, source)
            self.assertIn("$A_%d$" % vertex, source)
        self.assertIn("coordinate[pos=0.45] (P)", source)
        self.assertIn("its exact position is not specified", source)
        self.assertIn("\\draw[->] (A1) -- (A3);", source)
        self.assertIn("\\draw[->] (A1) -- (P);", source)
        self.assertIn(
            "P 的绘制点仅为示意位置，不表示精确位置。",
            FIGURE_LIST.read_text(encoding="utf-8"),
        )

    def test_q17_distinguishes_hidden_prism_edges_from_auxiliary_segments(self):
        source = (FIGURE_DIR / FIGURES[17]).read_text(encoding="utf-8")
        for start, end in (("A", "D"), ("D", "C"), ("D", "D1"), ("A1", "C"), ("A1", "D")):
            self.assertIn(r"\draw[dashed] (%s) -- (%s);" % (start, end), source)
        self.assertIn(r"\draw (A1) -- (B);", source)
        self.assertIn(r"\draw (D1) -- (A1);", source)
        for label in ("A", "B", "C", "D", "A_1", "B_1", "C_1", "D_1"):
            self.assertIn("$%s$" % label, source)

    def test_q19_preserves_right_angle_equal_segments_tangencies_and_centres(self):
        source = (FIGURE_DIR / FIGURES[19]).read_text(encoding="utf-8")
        self.assertIn(r"\coordinate (B) at (\L,0);", source)
        self.assertIn(r"\coordinate (C) at (0,\L);", source)
        self.assertIn(r"\coordinate (D) at (\Dxx,\Dyy);", source)
        self.assertIn(r"\coordinate (Mone) at (\L,\rOne);", source)
        self.assertIn(r"\coordinate (Mtwo) at (\rTwo,\L);", source)
        self.assertIn(r"\draw (A) -- (B) (A) -- (C) (A) -- (D);", source)
        self.assertIn(r"\fill (Mone) circle (1.2pt);", source)
        self.assertIn(r"\fill (Mtwo) circle (1.2pt);", source)
        self.assertIn("不标示意角度", source)

    def test_q19_places_circle_labels_outside_the_circle_bodies(self):
        source = (FIGURE_DIR / FIGURES[19]).read_text(encoding="utf-8")
        self.assertIn(
            r"\coordinate (MoneLabel) at ({\L+0.72*\rOne},{\rOne+0.72*\rOne});",
            source,
        )
        self.assertIn(r"\node[above right=2pt] at (MoneLabel) {$M_1$};", source)
        self.assertIn(r"\coordinate (MtwoLabel) at (\rTwo,{\L+\rTwo});", source)
        self.assertIn(r"\node[above=2pt] at (MtwoLabel) {$M_2$};", source)

    def test_q19_layout_does_not_encode_a_numeric_angle_parameter(self):
        source = (FIGURE_DIR / FIGURES[19]).read_text(encoding="utf-8")
        self.assertNotRegex(source, r"\\theta|(?:cos|sin)\s*\(")
        self.assertIn("numerical coordinates are only a schematic layout", source)

    def test_reviewed_diagrams_are_resolved_nonblocking_issues(self):
        sys.path.insert(0, str(PROJECT / "tools"))
        import issues

        paper_issues = [
            item
            for item in issues.load_issues(PROJECT / "missing-issues.md")
            if item.get("paper_id") == PAPER_ID and item.get("type") == "figure-missing"
        ]
        self.assertEqual({item["question_id"] for item in paper_issues}, {
            PAPER_ID + "-q16", PAPER_ID + "-q17", PAPER_ID + "-q19"
        })
        self.assertTrue(all(item["status"] == "resolved" for item in paper_issues))
        self.assertTrue(all(item["impact"] == "non_blocking" for item in paper_issues))


if __name__ == "__main__":
    unittest.main()
