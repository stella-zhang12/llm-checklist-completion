"""Input source file discovery/loading utilities."""

import os

import pandas as pd

from pipeline_config import DATA_DIR, DATA_FILE_EXTENSIONS


def resolve_source_file(data_dir=DATA_DIR):
    """Resolve a single source file from the data directory."""
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    candidates = []
    for name in sorted(os.listdir(data_dir)):
        path = os.path.join(data_dir, name)
        if not os.path.isfile(path):
            continue
        lower_name = name.lower()
        if lower_name.endswith(DATA_FILE_EXTENSIONS):
            candidates.append(path)

    if not candidates:
        allowed = ", ".join(DATA_FILE_EXTENSIONS)
        raise FileNotFoundError(
            f"No source file found in '{data_dir}'. Add one file with extension: {allowed}"
        )

    if len(candidates) > 1:
        file_list = ", ".join(os.path.basename(path) for path in candidates)
        raise ValueError(
            f"Multiple source files found in '{data_dir}': {file_list}. Keep only one source file."
        )

    return candidates[0]


def load_source_dataframe(source_file):
    """Load source data from CSV or Excel into a DataFrame."""
    lower_file = source_file.lower()
    if lower_file.endswith(".csv"):
        return pd.read_csv(source_file)
    if lower_file.endswith((".xlsx", ".xls")):
        return pd.read_excel(source_file)
    raise ValueError(f"Unsupported source file format: {source_file}")
