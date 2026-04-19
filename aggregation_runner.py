"""Shared aggregation engine for ENG and VIET result directories."""

import json
import os

import pandas as pd


def aggregate_model_results(*, results_dir, output_file, coder_prefix):
    all_rows = []

    if not os.path.exists(results_dir):
        print(f"Error: Directory '{results_dir}' not found.")
        return

    model_folders = [
        directory
        for directory in os.listdir(results_dir)
        if os.path.isdir(os.path.join(results_dir, directory))
    ]

    if not model_folders:
        print(f"No model subdirectories found in '{results_dir}'.")
        if any(filename.endswith(".json") for filename in os.listdir(results_dir)):
            model_folders = ["."]
        else:
            return

    print(f"Found model folders: {model_folders}")

    for folder_name in model_folders:
        folder_path = os.path.join(results_dir, folder_name)

        if folder_name == ".":
            coder_id = f"{coder_prefix}-Unknown"
        else:
            coder_id = f"{coder_prefix}-{folder_name}"

        files = sorted([filename for filename in os.listdir(folder_path) if filename.endswith(".json")])
        print(f"Processing {len(files)} files in '{folder_name}'...")

        for filename in files:
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                basename = os.path.splitext(filename)[0]
                parts = basename.split("__")

                prefix = "UNK"
                patient_name = basename
                case_id = "UNK"

                if len(parts) >= 3:
                    prefix = parts[0]
                    patient_name = parts[1]
                    case_id = parts[2]
                elif len(parts) == 2:
                    prefix = parts[0]
                    patient_name = parts[1]

                row_dict = {
                    "coder": coder_id,
                    "Prefix": prefix,
                    "Patient_Name": patient_name,
                    "Case_ID": case_id,
                    "Filename": filename,
                }

                if "results" in data and isinstance(data["results"], list):
                    for item in data["results"]:
                        var_name = item.get("output_variable")
                        val = item.get("value")
                        if var_name:
                            row_dict[var_name] = val
                else:
                    for key, value in data.items():
                        if key != "results":
                            row_dict[key] = value

                all_rows.append(row_dict)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON in {filename}. Skipping.")
            except Exception as exc:
                print(f"Error processing {filename}: {exc}")

    if not all_rows:
        print("No valid data found to aggregate.")
        return

    df = pd.DataFrame(all_rows)
    meta_cols = ["coder", "Prefix", "Patient_Name", "Case_ID", "Filename"]
    variable_cols = sorted([col for col in df.columns if col not in meta_cols])
    final_cols = [col for col in (meta_cols + variable_cols) if col in df.columns]

    df = df[final_cols]

    try:
        df.to_excel(output_file, index=False)
        print(f"\nSuccess! Aggregated data saved to '{output_file}'")
        print(f"Total Rows: {len(df)}")
        print(f"Unique Models: {df['coder'].unique()}")
    except Exception as exc:
        print(f"Error saving Excel file: {exc}")
