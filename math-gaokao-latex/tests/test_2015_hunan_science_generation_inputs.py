import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "math-gaokao-latex/tools"))

from solution_sources import (  # noqa: E402
    SolutionSourceError,
    extract_solution_blocks,
    parse_answer_points,
    parse_question_blocks,
    render_combined,
)
from generate_projects import ProjectSources, generate_project, validate_project_result  # noqa: E402


QUESTIONS = ROOT / "2015/2015_数学真题_湖南理_试题.md"
SOLUTION = ROOT / "2015/2015_数学真题_湖南理_数学独立推导草稿.md"
ANSWER_KEY = ROOT / "2015/2015_数学真题_湖南理_答案要点.md"
CONVERTER = ROOT / "math-gaokao-2017-2026/tools/md2tex.py"
REVIEW = ROOT / "2015/2015_湖南理科_来源校对.json"


class HunanScienceGenerationInputTests(unittest.TestCase):
    def test_review_receipt_tracks_hashes_and_nonofficial_answer_status(self):
        review = json.loads(REVIEW.read_text(encoding="utf-8"))
        for section, path in (
            ("question_transcript", QUESTIONS),
            ("generated_solution", SOLUTION),
            ("generated_answer_key", ANSWER_KEY),
        ):
            self.assertEqual(
                review[section]["sha256"],
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
        self.assertEqual(
            review["generated_answer_key"]["status"], "generated-nonofficial-draft"
        )

    def test_question_and_solution_subpart_anchors_align(self):
        questions = parse_question_blocks(QUESTIONS.read_text(encoding="utf-8"))
        solutions = parse_question_blocks(SOLUTION.read_text(encoding="utf-8"))
        expected = {number: (1, 2) for number in range(16, 22)}
        for number, subparts in expected.items():
            self.assertEqual(questions[number - 1].subparts, subparts)
            self.assertEqual(solutions[number - 1].subparts, subparts)

    def test_solution_body_has_one_block_per_printed_question(self):
        try:
            blocks = parse_question_blocks(SOLUTION.read_text(encoding="utf-8"))
        except SolutionSourceError as exc:
            self.fail(f"the formal solution source must contain unique paper question blocks: {exc}")
        self.assertEqual([block.number for block in blocks], list(range(1, 22)))
        optional = blocks[15].body
        for variant in ("【A】", "【B】", "【C】"):
            self.assertIn(variant, optional)

    def test_answer_key_covers_all_questions_and_preserves_unofficial_branches(self):
        self.assertTrue(ANSWER_KEY.is_file(), "a separately sourced answer-key input is required")
        answer_text = ANSWER_KEY.read_text(encoding="utf-8")
        points = parse_answer_points(answer_text)
        self.assertEqual([point.number for point in points], list(range(1, 22)))
        self.assertEqual(points[15].subparts, (1, 2))
        q14 = points[13].answers[0][1]
        self.assertIn(r"q=0", q14)
        self.assertIn(r"q=3", q14)
        self.assertIn("非官方", answer_text)
        q16 = points[15].answers[0][1]
        for variant in ("A", "B", "C"):
            self.assertIn(variant, q16)

    def test_real_generator_and_latex_converter_accept_all_three_sources(self):
        question_text = QUESTIONS.read_text(encoding="utf-8")
        solution_text = SOLUTION.read_text(encoding="utf-8")
        answer_text = ANSWER_KEY.read_text(encoding="utf-8")
        body = extract_solution_blocks(solution_text, question_text)
        combined = render_combined(question_text, body, answer_text)

        spec = importlib.util.spec_from_file_location("gaokao_md2tex", CONVERTER)
        md2tex = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(md2tex)
        links = re.findall(r"\[[^\]]+\]\(([^)]+\.tex)\)", question_text)
        figure_map = {link: Path(link).stem for link in links}
        converted = md2tex.convert_markdown(
            combined, md2tex.ConversionContext(figure_map=figure_map, strict=True)
        )
        self.assertEqual(converted.warnings, ())
        self.assertEqual(set(converted.referenced_figures), set(figure_map.values()))
        self.assertEqual(len(converted.referenced_figures), len(links))

    def test_formal_project_generator_accepts_registered_figure_paths(self):
        project_dir = "2015_湖南卷_理科"
        vector_dir = ROOT / "math-gaokao-latex/2015_湖南卷_理科/figures"
        vector_files = sorted(vector_dir.glob("*.tex"))
        figures = tuple(
            (f"{project_dir}/figures/{path.name}", 2) for path in vector_files
        )
        sources = ProjectSources(
            paper_id="gk-2015-regular-hunan-science",
            project_dir=project_dir,
            title="2015 年·湖南卷·理科",
            question_count=21,
            questions=QUESTIONS.relative_to(ROOT).as_posix(),
            answer_key=ANSWER_KEY.relative_to(ROOT).as_posix(),
            solution_body=SOLUTION.relative_to(ROOT).as_posix(),
            figures=figures,
        )
        with tempfile.TemporaryDirectory(prefix="hunan-science-generation-") as temp:
            repo = Path(temp)
            for source in (QUESTIONS, ANSWER_KEY, SOLUTION):
                target = repo / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            for source in vector_files:
                target = (
                    repo / "math-gaokao-latex" / project_dir
                    / "figures" / source.name
                )
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)

            result = generate_project(repo, sources)
            self.assertEqual(validate_project_result(sources, result), ())
            self.assertEqual(
                set(result.targets),
                {
                    f"math-gaokao-latex/{project_dir}/questions.tex",
                    f"math-gaokao-latex/{project_dir}/answers.tex",
                },
            )


if __name__ == "__main__":
    unittest.main()
