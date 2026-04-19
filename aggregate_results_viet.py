"""Vietnamese aggregation entrypoint."""

from aggregation_runner import aggregate_model_results
from pipeline_config import AGGREGATED_VIET_OUTPUT, RESULTS_VIET_DIR


def aggregate_results_viet():
    aggregate_model_results(
        results_dir=RESULTS_VIET_DIR,
        output_file=AGGREGATED_VIET_OUTPUT,
        coder_prefix="VIET",
    )


if __name__ == "__main__":
    aggregate_results_viet()
