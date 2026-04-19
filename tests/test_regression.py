import json
import shutil
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from aggregation_runner import aggregate_model_results
from extract_transcript_text import make_transcripts_one_lang


REPO_ROOT = Path(__file__).resolve().parents[1]


class PipelineRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="llm-checklist-tests-"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_extract_keeps_duplicate_rows_with_versioned_filenames(self):
        df = pd.DataFrame(
            [
                {
                    "name": "PT-25-001",
                    "province": "A",
                    "district": "B",
                    "duration": 12,
                    "case_1_condition": "pne",
                    "custom_system_chat1_eng": '[{"role":"user","content":"How long has cough lasted?"}]',
                    "patient_1_diagnosis_eng": "Pneumonia",
                    "patient_1_treatment_eng": "Ceftriaxone",
                    "patient_1_treatment_post_eng": "Monitor and follow up",
                },
                {
                    "name": "PT-25-001",
                    "province": "A",
                    "district": "B",
                    "duration": 14,
                    "case_1_condition": "pne",
                    "custom_system_chat1_eng": '[{"role":"user","content":"Any chest pain?"}]',
                    "patient_1_diagnosis_eng": "Pneumonia",
                    "patient_1_treatment_eng": "Ceftriaxone",
                    "patient_1_treatment_post_eng": "Monitor and follow up",
                },
            ]
        )

        output_dir = self.tmpdir / "transcripts_text_eng"
        make_transcripts_one_lang(df, str(output_dir), "eng")

        generated_files = sorted(path.name for path in output_dir.glob("*.txt"))
        self.assertEqual(
            generated_files,
            [
                "pne__PT-25-001__case_1.txt",
                "pne__PT-25-001__case_1__v2.txt",
            ],
        )

        first_contents = (output_dir / "pne__PT-25-001__case_1.txt").read_text(encoding="utf-8")
        self.assertIn("User inputs:", first_contents)
        self.assertIn("Other fields:", first_contents)

    def test_aggregate_produces_expected_metadata_columns(self):
        results_dir = self.tmpdir / "results" / "gpt-4.1"
        results_dir.mkdir(parents=True)

        fixture = REPO_ROOT / "tests" / "fixtures" / "sample_result.json"
        payload = json.loads(fixture.read_text(encoding="utf-8"))

        output_json = results_dir / "pne__PT-25-001__case_1.json"
        output_json.write_text(json.dumps(payload), encoding="utf-8")

        output_excel = self.tmpdir / "aggregated_results.xlsx"
        aggregate_model_results(
            results_dir=str(self.tmpdir / "results"),
            output_file=str(output_excel),
            coder_prefix="ENG",
        )

        self.assertTrue(output_excel.exists())
        df = pd.read_excel(output_excel)
        for required_col in ["coder", "Prefix", "Patient_Name", "Case_ID", "Filename", "pne_h_1", "pne_d"]:
            self.assertIn(required_col, df.columns)
        self.assertEqual(df.loc[0, "coder"], "ENG-gpt-4.1")

    def test_makefile_run_target_wiring(self):
        makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("run: extract analyze analyze-viet aggregate aggregate-viet", makefile)
        self.assertIn("aggregate-viet:", makefile)
        self.assertIn("Run full pipeline for ENG and VIET outputs", makefile)


if __name__ == "__main__":
    unittest.main()
