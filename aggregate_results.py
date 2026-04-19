"""English aggregation entrypoint."""

from aggregation_runner import aggregate_model_results
from pipeline_config import AGGREGATED_ENG_OUTPUT, RESULTS_ENG_DIR


def aggregate_results():
    aggregate_model_results(
        results_dir=RESULTS_ENG_DIR,
        output_file=AGGREGATED_ENG_OUTPUT,
        coder_prefix="ENG",
    )


if __name__ == "__main__":
    aggregate_results()
