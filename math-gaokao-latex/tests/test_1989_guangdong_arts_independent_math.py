import hashlib
import json
import re
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = PROJECT / "1989_广东卷_文科"
INDEPENDENT = ROOT / "1989/1989_数学真题_广东文_独立解答草稿.md"
ANSWERS = ROOT / "1989/1989_数学真题_广东文_答案要点草稿.md"
QUESTIONS = ROOT / "1989/1989_数学真题_广东文_试题.md"
RECORD = PAPER / "来源校对.json"
PROGRESS = PROJECT / "PROGRESS.md"
SECOND_VOLUME_EXPECTED = (
    ("I-1", "-1"),
    ("I-2", "y=(1-x)/(3x), x!=0"),
    ("I-3", "3x+sqrt(3)y=12"),
    ("I-4", "1/2"),
    ("I-5", "23"),
    ("II-1", "geometric, ratio=a^d"),
    ("II-2", "x=-1/2"),
    ("III-1", "AC=BC"),
    ("III-2", "SC=5cm"),
    ("IV-1", "-1-i; modulus=sqrt(2), argument=5pi/4"),
    ("IV-2", "a in (-1,-1/2] U [-1/5,+inf)"),
    ("V-1", "x^2+(y+1)^2/4=1"),
    ("V-2", "theta=0,pi; Lmax=2"),
)


class GuangdongArtsIndependentMathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.independent = INDEPENDENT.read_text(encoding="utf-8") if INDEPENDENT.is_file() else ""
        cls.answers = ANSWERS.read_text(encoding="utf-8") if ANSWERS.is_file() else ""
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.progress = PROGRESS.read_text(encoding="utf-8") if PROGRESS.is_file() else ""

    def test_derived_results_are_separate_and_never_called_official(self):
        self.assertEqual(self.record.get("official_answer"), None)
        self.assertEqual(
            self.record.get("generated_answer_attribution"),
            "agent-derived-unverified-not-official",
        )
        self.assertEqual(self.record.get("mathematical_verification_status"), "conditionally-reviewed-with-source-conditions")
        self.assertEqual(self.record.get("verification", {}).get("independent_math_review", {}).get("status"), "conditional-pass")
        self.assertTrue("非官方独立推导" in self.independent)
        self.assertTrue(r"\left(-1,-\frac12\right]\cup\left[-\frac15,+\infty\right)" in self.independent)
        self.assertTrue(r"\theta=0\ \text{或}\ \pi" in self.independent)
        self.assertTrue(r"\boxed{\theta=0\ \text{或}\ \pi}" in self.independent)
        self.assertTrue(r"\left(-1,-\frac12\right]" not in self.answers)
        self.assertTrue(r"\theta=0,\pi" not in self.answers)

    def test_quadratic_factorization_and_domain_match_the_solution_intervals(self):
        samples = (
            Fraction(-1, 1), Fraction(-9, 10), Fraction(-3, 4),
            Fraction(-1, 2), Fraction(-3, 8), Fraction(-1, 5),
            Fraction(-3, 20), Fraction(0), Fraction(2),
        )
        for a in samples:
            with self.subTest(a=a):
                polynomial = 10 * a * a + 7 * a + 1
                self.assertEqual(polynomial, (5 * a + 1) * (2 * a + 1))
                domain = a > -1
                factored_solution = a <= Fraction(-1, 2) or a >= Fraction(-1, 5)
                self.assertEqual(domain and polynomial >= 0, domain and factored_solution)

    def test_chord_length_squared_decreases_with_sine_squared(self):
        def length_squared(u):
            return 4 * (1 - u) / (1 + 3 * u)

        values = (Fraction(0), Fraction(1, 16), Fraction(1, 4), Fraction(3, 4), Fraction(1))
        self.assertEqual(length_squared(Fraction(0)), 4)
        self.assertEqual(length_squared(Fraction(1)), 0)
        for smaller, larger in zip(values, values[1:]):
            with self.subTest(smaller=smaller, larger=larger):
                self.assertGreater(length_squared(smaller), length_squared(larger))

    def test_question_nine_answer_key_conflict_is_explicit_and_unresolved(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        self.assertIn("象集合的元素 $(y-1,x+2)$", questions)
        self.assertIn("B．$(-6,4)$", questions)

        rows = re.findall(r"^\|\s*(\d+)\s*\|\s*([ABCD])\s*\|", self.answers, re.MULTILINE)
        self.assertEqual(dict((int(number), answer) for number, answer in rows)[9], "C")

        image = (3, -4)
        preimage = (-6, 4)
        self.assertEqual((preimage[1] - 1, preimage[0] + 2), image)
        self.assertNotEqual((2 - 1, 2 + 2), image)

        conflicts = self.record.get("source_discrepancies", [])
        q9 = next((item for item in conflicts if item.get("question_number") == 9), None)
        self.assertIsNotNone(q9, "question 9 source/key conflict is not recorded")
        self.assertEqual(q9.get("question_source_page"), 3)
        self.assertEqual(q9.get("answer_source_page"), 8)
        self.assertEqual(q9.get("printed_answer"), "C")
        self.assertEqual(q9.get("answer_from_transcribed_mapping"), "B")
        self.assertEqual(q9.get("status"), "unresolved-source-conflict")
        source_review = self.record.get("verification", {}).get("q9_q12_focused_source_reinspection", {})
        self.assertEqual(source_review.get("status"), "passed-with-q9-conflict-open")
        self.assertEqual(source_review.get("source_sha256"), "e0b112f4d4576e791844332f7ffb465c65f3a3ba6516467a7888f9333ca7169f")
        self.assertEqual(source_review.get("source_pages"), [3, 8])
        self.assertEqual((source_review.get("q9_stem_answer"), source_review.get("q9_printed_key")), ("B", "C"))
        self.assertTrue(source_review.get("q9_transcription_matches_source"))
        self.assertEqual(source_review.get("q12_option_mapping"), "B")
        self.assertEqual(source_review.get("report"), "reports/1989-guangdong-arts-q9-source-reinspection.md")
        self.assertTrue(
            "1989 广东卷文科：第9题来源答案冲突核查" in self.progress,
            "missing Q9 source-conflict progress receipt",
        )

    def test_identical_public_mirror_does_not_upgrade_provenance_or_resolve_q9(self):
        mirror = self.record.get("external_catalog_match", {})
        self.assertEqual(mirror.get("repository_path"), "普通高考/1989/1989广东文.pdf")
        self.assertEqual(mirror.get("github_blob_oid"), "ee0f4dfcd5af015b510348df03671c224630d9e4")
        self.assertEqual(mirror.get("match_kind"), "identical-file-mirror-only")
        self.assertFalse(mirror.get("independent_source"))
        self.assertEqual(self.record["source"]["source_authenticity"], "unverified")
        self.assertTrue(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["source"]["paper_relation"], "canonical")
        q9 = next(item for item in self.record["source_discrepancies"] if item["question_number"] == 9)
        self.assertEqual(q9["status"], "unresolved-source-conflict")
        self.assertTrue("1989 广东卷文科：公开目录同源文件核对" in self.progress)
        leads = self.record.get("bibliographic_leads", [])
        book = next((item for item in leads if item.get("isbn") == "9787532019052"), None)
        self.assertIsNotNone(book, "contemporary book record should remain a traceable lead")
        self.assertEqual(book.get("evidence_level"), "secondary-catalog-metadata-only")
        self.assertFalse(book.get("content_pages_verified"))
        self.assertFalse(book.get("matches_fixed_pdf"))
        self.assertEqual(book.get("source_authenticity_effect"), "none")
        self.assertEqual(book.get("q9_resolution_effect"), "none")
        self.assertEqual(self.record["source"]["source_authenticity"], "unverified")
        self.assertTrue(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["source"]["paper_relation"], "canonical")
        self.assertTrue("1989 广东卷文科：同期书目线索登记" in self.progress)

    def test_catalog_access_block_is_not_misreported_as_no_record_or_verified_source(self):
        checks = self.record.get("catalog_checks", [])
        shanghai = next(
            (item for item in checks if item.get("catalog") == "Shanghai Library OPAC"),
            None,
        )
        self.assertIsNotNone(shanghai, "official Shanghai Library OPAC attempt is not recorded")
        self.assertEqual(shanghai.get("query"), "ISBN 9787532019052")
        self.assertEqual(shanghai.get("result_state"), "access-verification-blocked")
        self.assertIsNone(shanghai.get("record_found"))
        self.assertEqual(shanghai.get("source_authenticity_effect"), "none")
        self.assertEqual(shanghai.get("q9_resolution_effect"), "none")

        nlc = next(
            (item for item in checks if item.get("catalog") == "National Library of China OPAC"),
            None,
        )
        self.assertIsNotNone(nlc, "official NLC OPAC connection failure is not recorded")
        self.assertEqual(nlc.get("result_state"), "endpoint-unreachable-before-search")
        self.assertIsNone(nlc.get("record_found"))

        pdc = next(
            (item for item in checks if item.get("catalog") == "National Version Data Center PDC"),
            None,
        )
        self.assertIsNotNone(pdc, "official PDC login boundary is not recorded")
        self.assertEqual(pdc.get("query"), "ISBN 9787532019052 (search blocked by login redirect)")
        self.assertEqual(pdc.get("result_state"), "login-required-before-search")
        self.assertIsNone(pdc.get("record_found"))
        self.assertEqual(pdc.get("source_authenticity_effect"), "none")
        self.assertEqual(pdc.get("q9_resolution_effect"), "none")
        self.assertEqual(self.record["source"]["source_authenticity"], "unverified")
        self.assertEqual(self.record["exam"]["paper_id"], "gk-1989-regular-guangdong-arts")
        self.assertTrue(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["source"]["paper_relation"], "canonical")
        q9 = next(item for item in self.record["source_discrepancies"] if item["question_number"] == 9)
        self.assertEqual(q9["status"], "unresolved-source-conflict")
        self.assertTrue("1989 广东文科来源核查：公共馆藏目录访问结果" in self.progress)

    def test_second_volume_subquestions_are_recomputed_and_conditionally_reviewed(self):
        rows = re.findall(
            r"^\|\s*(I-\d+|II-\d+|III-\d+|IV-\d+|V-\d+)\s*\|\s*([^|]+?)\s*\|",
            self.independent,
            re.MULTILINE,
        )
        self.assertEqual(rows, list(SECOND_VOLUME_EXPECTED))

        artifact = self.record.get("artifacts", {}).get("independent_solution_draft", {})
        self.assertEqual(artifact.get("questions"), [item for item, _ in SECOND_VOLUME_EXPECTED])
        self.assertEqual(artifact.get("attribution"), "agent-derived-unverified-not-official")
        self.assertEqual(self.record.get("official_answer"), None)
        self.assertEqual(self.record.get("mathematical_verification_status"), "conditionally-reviewed-with-source-conditions")
        self.assertEqual(self.record.get("verification", {}).get("independent_math_review", {}).get("status"), "conditional-pass")
        self.assertTrue(
            "1989 广东卷文科：第二卷独立复算" in self.progress,
            "missing second-volume progress receipt",
        )

    def test_independent_draft_hash_and_progress_receipt(self):
        artifact = self.record.get("artifacts", {}).get("independent_solution_draft", {})
        self.assertTrue(INDEPENDENT.is_file())
        self.assertEqual(artifact.get("path"), str(INDEPENDENT.relative_to(ROOT)))
        self.assertEqual(artifact.get("sha256"), hashlib.sha256(INDEPENDENT.read_bytes()).hexdigest())
        self.assertTrue(
            "1989 广东卷文科：缺失答案独立推导" in self.progress,
            "missing independent-derivation progress receipt",
        )
        self.assertTrue(
            "test_1989_guangdong_arts_independent_math.py" in self.progress,
            "progress omits the math test",
        )


if __name__ == "__main__":
    unittest.main()
