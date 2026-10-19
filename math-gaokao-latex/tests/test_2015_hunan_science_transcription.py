import csv
import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2015/2015_数学真题_湖南理_试题.md"
FIGURES = ROOT / "2015/2015_数学真题_湖南理_图形清单.md"
REVIEW = ROOT / "2015/2015_湖南理科_来源校对.json"
MANIFEST = ROOT / "math-gaokao-latex/manifest.csv"
ISSUES = ROOT / "math-gaokao-latex/missing-issues.md"
sys.path.insert(0, str(ROOT / "math-gaokao-latex/tools"))
import issues


class HunanScienceTranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        cls.figures = FIGURES.read_text(encoding="utf-8")
        cls.review = json.loads(REVIEW.read_text(encoding="utf-8"))

    def test_manifest_source_is_bound_to_blocked_draft_and_hash_matches(self):
        source_id = self.review["source"]["source_id"]
        paper_id = "gk-2015-regular-hunan-science"
        with MANIFEST.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        source = next(row for row in rows if row["source_id"] == source_id)

        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(self.review["paper_id"], paper_id)
        self.assertEqual(source["paper_id"], paper_id)
        self.assertEqual(source["paper_relation"], "canonical")
        self.assertEqual(source["production_state"], "blocked")
        self.assertEqual(source["source_sha256"], self.review["source"]["sha256"])
        self.assertEqual(self.review["source"]["pdf_pages"], 2)
        self.assertEqual(self.review["source"]["printed_pages"], [955, 956])
        issue, = [item for item in issues.load_issues(ISSUES)
                  if item.get("paper_id") == paper_id]
        self.assertEqual(issue["type"], "answer-convention-ambiguous")
        self.assertEqual(issue["question_id"], paper_id + "-q14")
        self.assertEqual(issue["source_id"], source_id)
        self.assertEqual(
            hashlib.sha256(TRANSCRIPT.read_bytes()).hexdigest(),
            self.review["question_transcript"]["sha256"],
        )

    def test_all_21_questions_are_present_in_three_source_sections(self):
        numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 22)))
        self.assertEqual(self.review["question_transcript"]["question_numbers"], numbers)
        self.assertEqual(self.review["question_transcript"]["question_types"], {
            "single_choice": list(range(1, 11)),
            "fill_in": list(range(11, 16)),
            "written_response": list(range(16, 22)),
        })

    def test_high_risk_source_expressions_and_q14_definition_review_are_recorded(self):
        for expression in (
            r"2x-y\leqslant 1",
            r"x^{\frac32}",
            r"\overrightarrow{PA}+\overrightarrow{PB}+\overrightarrow{PC}",
            r"3S_1,2S_2,S_3",
            r"\overrightarrow{AC}\) 与 \(\overrightarrow{BD}",
            r"\dfrac{1}{\sqrt{e^2-1}}",
        ):
            self.assertIn(expression, self.transcript)
        self.assertIsNone(self.review["official_answer"]["value"])
        self.assertEqual(self.review["official_answer"]["status"], "not-present-in-fixed-source")
        self.assertEqual(
            self.review["generated_solution"]["status"],
            "draft-partially-blind-reviewed",
        )
        solution_path = ROOT / self.review["generated_solution"]["path"]
        self.assertEqual(
            hashlib.sha256(solution_path.read_bytes()).hexdigest(),
            self.review["generated_solution"]["sha256"],
        )
        self.assertEqual(
            self.review["generated_solution"]["independent_review_status"],
            "partial-full-paper-review-pending",
        )
        self.assertEqual(
            self.review["generated_solution"]["independent_reviewed_questions"],
            list(range(1, 16)) + [17, 18, 19, 20, 21],
        )
        self.assertEqual(
            self.review["generated_solution"]["independent_reviewed_subparts"],
            ["Q16A", "Q16B", "Q16C"],
        )
        self.assertEqual(
            self.review["generated_solution"]["unresolved_review_items"],
            [
                "Q14 intended geometric-sequence convention is not established by the fixed source; retain both conditional branches pending traceable source evidence."
            ],
        )
        self.assertTrue(any(
            "Q14" in note and "a_3/a_2" in note
            for note in self.review["generated_solution"]["independent_review_notes"]
        ))
        ledger = (ROOT / "2015/2015_数学真题_湖南理_盲核对账草稿.md").read_text(encoding="utf-8")
        self.assertIn(r"\(n=3\)时求和为\(1/3+1/15+1/35=3/7\)", ledger)
        self.assertIn("a_3/a_2", ledger)
        self.assertIn("原题意图和官方答案仍待来源核实", ledger)

    def test_stem_leaf_data_is_transcribed_without_omissions_or_reordering(self):
        body = re.search(
            r"\\begin\{array\}\{c\|l\}\s*(.*?)\\end\{array\}",
            self.transcript,
            re.S,
        ).group(1)
        rows = {}
        for line in body.splitlines():
            if "&" in line:
                stem, leaves = line.split("&", 1)
                rows[stem.strip()] = re.findall(r"\d+", leaves)
        self.assertEqual(rows, {
            "13": ["0", "0", "3", "4", "5", "6", "6", "8", "8", "8", "9"],
            "14": ["1", "1", "1", "2", "2", "2", "3", "3", "4", "4", "5", "5", "5", "6", "6", "7", "8"],
            "15": ["0", "1", "2", "2", "3", "3", "3"],
        })
        self.assertEqual(sum(map(len, rows.values())), 35)

    def test_source_footnote_and_all_vector_figures_are_embedded(self):
        self.assertIn(r"P(\mu-\sigma<X\leqslant\mu+\sigma)=0.6826", self.transcript)
        self.assertIn(r"P(\mu-2\sigma<X\leqslant\mu+2\sigma)=0.9544", self.transcript)
        links = re.findall(r"\[[^\]]+\]\(([^)]+\.tex)\)", self.transcript)
        self.assertEqual(len(links), 5)
        self.assertEqual({Path(link).name for link in links}, {
            "f2015hns_q03_flow.tex",
            "f2015hns_q07_normal_density.tex",
            "f2015hns_q10_cone_views.tex",
            "f2015hns_q16a_circle_chords.tex",
            "f2015hns_q19_frustum.tex",
        })
        fig16 = (ROOT / self.review["figures"]["vector_source_directory"] /
                 "f2015hns_q16a_circle_chords.tex").read_text(encoding="utf-8")
        self.assertIn(r"\coordinate (M) at (-.52,.26);", fig16)
        self.assertIn(r"\draw (O)--(N);", fig16)
        self.assertNotIn(r"\draw[densely dotted] (O)--(N);", fig16)

    def test_every_original_figure_is_in_inventory_and_not_committed_as_raster(self):
        self.assertNotIn("尚未重绘为规范图稿", self.transcript)
        self.assertNotIn("图稿完成并复核前，不生成可发布的正式版本", self.figures)
        self.assertIn("| 3 | 955 |", self.figures)
        for q in (7, 10, 12, "16A", 19):
            self.assertIn(f"| {q} |", self.figures)
        self.assertNotIn("| 待制作 |", self.figures)
        self.assertEqual(self.figures.count("独立源核无差异"), 3)
        self.assertIn("独立逐叶核对35/35一致", self.figures)
        self.assertIn("已修正M在FO上、ON为实线", self.figures)
        self.assertFalse(self.review["figures"]["source_raster_committed"])
        self.assertEqual(
            self.review["figures"]["vector_reconstruction_status"],
            "draft-source-reviewed-smoke-compiled",
        )
        visual_review = self.review["figures"]["independent_visual_review"]
        self.assertEqual(visual_review["question_numbers"], list(range(1, 22)))
        self.assertEqual(visual_review["figure_questions"], [3, 7, 10, 12, "16A", 19])
        self.assertEqual(visual_review["final_check_status"], "pending")
        vector_dir = ROOT / self.review["figures"]["vector_source_directory"]
        vector_files = sorted(vector_dir.glob("*.tex"))
        self.assertEqual(len(vector_files), 5)
        self.assertFalse(list(vector_dir.glob("*.png")))
        self.assertFalse(list(vector_dir.glob("*.jpg")))
        self.assertFalse(list(vector_dir.glob("*.jpeg")))
        for name, expected_sha in self.review["figures"]["vector_sources"].items():
            path = next(p for p in vector_files if f"_{name.lower()}_" in p.name)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected_sha)

    def test_local_tex_links_convert_to_registered_vector_inputs(self):
        module_path = ROOT / "math-gaokao-2017-2026/tools/md2tex.py"
        spec = importlib.util.spec_from_file_location("gaokao_md2tex", module_path)
        md2tex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(md2tex)
        links = re.findall(r"\[[^\]]+\]\(([^)]+\.tex)\)", self.transcript)
        figure_map = {link: Path(link).stem for link in links}
        result = md2tex.convert_markdown(
            self.transcript,
            md2tex.ConversionContext(figure_map=figure_map, strict=True),
        )
        self.assertEqual(
            result.referenced_figures,
            tuple(Path(link).stem for link in links),
        )
        self.assertEqual(result.warnings, ())


if __name__ == "__main__":
    unittest.main()
