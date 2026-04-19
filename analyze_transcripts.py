"""English analysis entrypoint."""

from analysis_runner import run_analysis
from pipeline_config import (
    ABLASTATS_ENG_FILE,
    MODELS_CONFIG,
    PROMPTS_PACKAGE,
    RESULTS_ENG_DIR,
    TOTAL_WORKERS,
    TRANSCRIPTS_ENG_DIR,
)


def main():
    run_analysis(
        input_dir=TRANSCRIPTS_ENG_DIR,
        output_dir=RESULTS_ENG_DIR,
        stats_file=ABLASTATS_ENG_FILE,
        models_config=MODELS_CONFIG,
        total_workers=TOTAL_WORKERS,
        prompts_package=PROMPTS_PACKAGE,
        scan_message="Scanning source files...",
        job_summary_title="--- JOB SUMMARY ---",
    )


if __name__ == "__main__":
    main()
