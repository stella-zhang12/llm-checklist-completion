import os
import json
import pandas as pd

# Configuration
RESULTS_DIR = "results"
OUTPUT_FILE = "aggregated_results.xlsx"

def aggregate_results():
    all_rows = []
    
    # 1. Check if directory exists
    if not os.path.exists(RESULTS_DIR):
        print(f"Error: Directory '{RESULTS_DIR}' not found.")
        return

    # 2. Find all model subdirectories (e.g., gpt-4.1, gpt-4.1-mini)
    # We look for folders inside 'results/'
    model_folders = [d for d in os.listdir(RESULTS_DIR) if os.path.isdir(os.path.join(RESULTS_DIR, d))]
    
    if not model_folders:
        print(f"No model subdirectories found in '{RESULTS_DIR}'.")
        # Fallback: check if there are JSONs in the root (legacy support)
        if any(f.endswith(".json") for f in os.listdir(RESULTS_DIR)):
            model_folders = ["."]
        else:
            return

    print(f"Found model folders: {model_folders}")

    # 3. Process each folder
    for folder_name in model_folders:
        folder_path = os.path.join(RESULTS_DIR, folder_name)
        
        # Define the "coder" ID based on the folder name
        # If folder is ".", assume generic or use directory name
        if folder_name == ".":
            coder_id = "ENG-Unknown"
        else:
            coder_id = f"ENG-{folder_name}"

        # Get JSON files in this folder
        files = sorted([f for f in os.listdir(folder_path) if f.endswith(".json")])
        print(f"Processing {len(files)} files in '{folder_name}'...")

        for filename in files:
            file_path = os.path.join(folder_path, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Parse filename metadata (format: prefix__name__case_X.json)
                basename = os.path.splitext(filename)[0]
                parts = basename.split("__")
                
                # Default values
                prefix = "UNK"
                patient_name = basename
                case_id = "UNK"
                
                # Robust extraction if filename matches pattern
                if len(parts) >= 3:
                    prefix = parts[0]
                    patient_name = parts[1]
                    case_id = parts[2]
                elif len(parts) == 2:
                    prefix = parts[0]
                    patient_name = parts[1]

                # Start row dictionary with Metadata + Coder
                row_dict = {
                    "coder": coder_id,           # <--- NEW COLUMN
                    "Prefix": prefix,
                    "Patient_Name": patient_name,
                    "Case_ID": case_id,
                    "Filename": filename
                }
                
                # Extract variables
                # Strategy 1: The 'results' list format (as in your reference)
                if "results" in data and isinstance(data["results"], list):
                    for item in data["results"]:
                        var_name = item.get("output_variable")
                        val = item.get("value")
                        if var_name:
                            row_dict[var_name] = val
                
                # Strategy 2: Flat JSON (fallback if structure changes)
                else:
                    for k, v in data.items():
                        if k not in ["results"]: # Avoid duplicating the list itself
                             row_dict[k] = v
                
                all_rows.append(row_dict)
                
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON in {filename}. Skipping.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # 4. Create DataFrame
    if not all_rows:
        print("No valid data found to aggregate.")
        return

    df = pd.DataFrame(all_rows)
    
    # Reorder columns: Metadata first
    meta_cols = ["coder", "Prefix", "Patient_Name", "Case_ID", "Filename"]
    
    # Identify variable columns (everything else) and sort them
    variable_cols = sorted([c for c in df.columns if c not in meta_cols])
    
    final_cols = meta_cols + variable_cols
    
    # Filter to ensure we only use columns that actually exist
    final_cols = [c for c in final_cols if c in df.columns]
    
    df = df[final_cols]

    # 5. Save to Excel
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"\nSuccess! Aggregated data saved to '{OUTPUT_FILE}'")
        print(f"Total Rows: {len(df)}")
        print(f"Unique Models: {df['coder'].unique()}")
    except Exception as e:
        print(f"Error saving Excel file: {e}")

if __name__ == "__main__":
    aggregate_results()