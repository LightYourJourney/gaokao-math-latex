import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2002/2002_数学真题_北京文_试题.md"
REVIEW = ROOT / "2002/2002_北京文科_来源校对.json"
FIGURES = ROOT / "2002/2002_数学真题_北京文_图表清单.md"
PAPER_ROOT = ROOT / "math-gaokao-latex/2002_北京卷_文科"
MANIFEST = ROOT / "math-gaokao-latex/source-manifest.json"
SOURCE_ID = "src-90f44916d96acc13cf570b10db11e0afffadc48c9f7139ba8411097f30f37449"
SOURCE_SHA = "65899ebe3859b55da2aa318d2ba79541675870468a89124240062b3e3d48c089"


class BeijingArts2002TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8") if TRANSCRIPT.is_file() else ""
        cls.review = json.loads(REVIEW.read_text(encoding="utf-8")) if REVIEW.is_file() else {}
        cls.figures = FIGURES.read_text(encoding="utf-8") if FIGURES.is_file() else ""
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_transcript_is_bound_to_the_exact_ready_unbound_source(self):
        self.assertTrue(TRANSCRIPT.is_file(), "题面转录尚未创建")
        self.assertTrue(REVIEW.is_file(), "来源回执尚未创建")
        source = next(s for s in self.manifest["sources"] if s["source_id"] == SOURCE_ID)
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["paper_id"], "gk-2002-regular-beijing-arts")
        self.assertEqual(source["paper_relation"], "canonical")
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(self.review["source_id"], SOURCE_ID)
        self.assertEqual(self.review["source"]["sha256"], SOURCE_SHA)
        self.assertEqual(self.review["source"]["printed_pages"], [102, 103])
        self.assertEqual(self.review["paper_id"], "gk-2002-regular-beijing-arts")
        self.assertIsNone(self.review["official_answer"])
        self.assertEqual(
            self.review["transcription"]["secondary_text_layer_cross_check"]["status"],
            "partial-text-layer-review-compared-to-source-raster",
        )
        self.assertEqual(
            self.review["transcription"]["visual_diff_resolutions"][0]["question_number"],
            8,
        )
        self.assertEqual(
            hashlib.sha256(TRANSCRIPT.read_bytes()).hexdigest(),
            self.review["transcription"]["sha256"],
        )

    def test_all_22_questions_are_in_printed_order_and_correct_sections(self):
        self.assertTrue(TRANSCRIPT.is_file(), "题面转录尚未创建")
        numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.review["transcription"]["question_count"], 22)
        self.assertEqual(
            self.review["transcription"]["question_types"],
            {
                "single_choice": list(range(1, 13)),
                "fill_in": list(range(13, 17)),
                "written_response": list(range(17, 23)),
            },
        )
        self.assertLess(self.transcript.index("**12．**"), self.transcript.index("## 二、填空题"))
        self.assertLess(self.transcript.index("**16．**"), self.transcript.index("## 三、解答题"))
        self.assertEqual(
            self.review["transcription"]["status"],
            "draft-transcribed-independently-reviewed",
        )
        self.assertEqual(self.review["transcription"]["independent_review"], "passed")
        self.assertEqual(
            self.review["figures_and_tables"]["vector_reconstruction_status"],
            "draft-independently-reviewed",
        )

    def test_source_high_risk_symbols_and_original_q15_duplicate_are_preserved(self):
        self.assertTrue(TRANSCRIPT.is_file(), "题面转录尚未创建")
        for expression in (
            r"\(M\cup\{1\}=\{1,2,3\}\)",
            r"\(|AB|\)",
            r"\(l:y=kx-\sqrt3\)",
            r"\dfrac{2\pi}{5}",
            r"\dfrac{6\pi}{5}",
            r"\dfrac{7\pi}{5}",
            r"（A）\(\dfrac{3}{5}\)　　（B）\(-\dfrac{3}{5}\)",
            r"x_{n+1}=\frac12\left(x_n+\frac{a}{x_n}\right)",
            r"x_n\geqslant\sqrt a",
            r"V_{\text{估}}=S_{\text{中截面}}\,h",
            r"V=\frac{h}{6}\left(S_{\text{上底面}}+4S_{\text{中截面}}+S_{\text{下底面}}\right)",
            r"f(a\cdot b)=a f(b)+b f(a)",
        ):
            self.assertIn(expression, self.transcript)
        self.assertEqual(self.transcript.count("④可能是直角"), 1)
        self.assertIn("原件 Q15 中③、④均印作“可能是直角”", self.transcript)

    def test_every_source_diagram_has_a_linked_tikz_asset_and_q20_tables_are_transcribed(self):
        self.assertTrue(TRANSCRIPT.is_file(), "题面转录尚未创建")
        self.assertTrue(REVIEW.is_file(), "来源回执尚未创建")
        expected = ["q4-cube-options", "q11-sign-graph", "q12-convexity-graphs", "q18-polyhedron"]
        self.assertEqual(self.review["figures_and_tables"]["items"], expected + ["q20-computation-tables"])
        assets = self.review["figures_and_tables"]["vector_assets"]
        self.assertEqual(len(assets), 4)
        for asset in assets:
            path = ROOT / asset["path"]
            self.assertTrue(path.is_file(), asset["path"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), asset["sha256"])
            source = path.read_text(encoding="utf-8")
            self.assertIn(r"\begin{tikzpicture}", source)
            self.assertIn(r"\end{tikzpicture}", source)
            self.assertIn(asset["path"].removeprefix("math-gaokao-latex/"), self.transcript)
        q12 = next(a for a in assets if a["item"] == "q12-convexity-graphs")
        q12_source = (ROOT / q12["path"]).read_text(encoding="utf-8")
        self.assertIn("change of concavity", q12_source)
        self.assertNotIn(r"\draw[fill=white] (2", q12_source)
        q4 = next(a for a in assets if a["item"] == "q4-cube-options")
        q4_source = (ROOT / q4["path"]).read_text(encoding="utf-8")
        for segment in (
            r"\draw[hidden edge] (h)--(b);",
            r"\draw[cube edge] (c)--(f);",
            r"\draw[hidden edge] (h)--(a);",
            r"\draw[cube edge] (d)--(b);",
            r"\draw[hidden edge] (d)--(e);",
            r"(g)--(f)--(b)",
            r"\draw[cube edge] (g)--(f);",
        ):
            self.assertIn(segment, q4_source)
        self.assertEqual(q4_source.count(r"\draw[hidden edge] (h)--(b);"), 2)
        q11 = next(a for a in assets if a["item"] == "q11-sign-graph")
        q11_source = (ROOT / q11["path"]).read_text(encoding="utf-8")
        self.assertIn("(1.00,0)", q11_source)
        self.assertIn("(2.94,.015)", q11_source)
        self.assertIn("单位时间", self.transcript)
        self.assertIn("被读机号", self.transcript)
        self.assertIn("机器号", self.transcript)
        self.assertNotIn("待独立复核", self.figures)
        self.assertFalse(self.review["figures_and_tables"]["raster_source_committed"])
        raster_suffixes = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff", ".bmp"}
        tracked_rasters = [p for p in PAPER_ROOT.rglob("*") if p.suffix.lower() in raster_suffixes]
        self.assertEqual(tracked_rasters, [])

    def test_math_delimiters_are_balanced_in_transcript_and_inventory(self):
        for text in (self.transcript, self.figures):
            self.assertEqual(text.count(r"\("), text.count(r"\)"))
            self.assertEqual(text.count(r"\["), text.count(r"\]"))

    @unittest.skipUnless(shutil.which("latexmk"), "latexmk is required")
    def test_each_tikz_asset_compiles_with_xelatex(self):
        for asset in self.review["figures_and_tables"]["vector_assets"]:
            with self.subTest(asset=asset["item"]), tempfile.TemporaryDirectory() as temp:
                wrapper = Path(temp) / "figure.tex"
                wrapper.write_text(
                    "\\documentclass{article}\n"
                    "\\usepackage{tikz}\n"
                    "\\pagestyle{empty}\n"
                    "\\begin{document}\n"
                    f"\\input{{{(ROOT / asset['path']).as_posix()}}}\n"
                    "\\end{document}\n",
                    encoding="utf-8",
                )
                result = subprocess.run(
                    ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
                    cwd=temp,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                self.assertEqual(result.returncode, 0, result.stdout[-3000:] + result.stderr[-3000:])
                self.assertTrue((Path(temp) / "figure.pdf").is_file())


if __name__ == "__main__":
    unittest.main()
