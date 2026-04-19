"""Vietnamese analysis entrypoint."""

from analysis_runner import run_analysis
from pipeline_config import (
    ABLASTATS_VIET_FILE,
    MODELS_CONFIG,
    PROMPTS_PACKAGE,
    RESULTS_VIET_DIR,
    TOTAL_WORKERS,
    TRANSCRIPTS_VIET_DIR,
)


def main():
    run_analysis(
        input_dir=TRANSCRIPTS_VIET_DIR,
        output_dir=RESULTS_VIET_DIR,
        stats_file=ABLASTATS_VIET_FILE,
        models_config=MODELS_CONFIG,
        total_workers=TOTAL_WORKERS,
        prompts_package=PROMPTS_PACKAGE,
        scan_message="Scanning source files in {input_dir}...",
        job_summary_title="--- JOB SUMMARY (VIETNAMESE) ---",
        require_input_dir=True,
    )


if __name__ == "__main__":
    main()
