import pandas as pd
import re
import os
import shutil

# ================================
# Configuration
# ================================
INPUT_FILE = "data/llm-data-baseline-1125-translated.xlsx - data.csv"
OUT_DIR_ENG = "transcripts_text_eng"
OUT_DIR_VIET = "transcripts_text_viet"
K_VALUES = range(1, 6)  # Cases 1 to 5

# ================================
# Helper Functions
# ================================

def safe_filename(x):
    """Sanitizes strings for use as filenames."""
    if pd.isna(x): return "UNKNOWN"
    x = str(x).strip()
    x = re.sub(r'[\\/*?:"<>|]', '_', x)
    x = re.sub(r'\s+', ' ', x)
    x = re.sub(r'_+', '_', x)
    return x.strip('_')[:120]

def make_unique_path(path):
    """
    If file exists (e.g., duplicate user), appends __v2, __v3, etc.
    This ensures we keep duplicates instead of overwriting them.
    """
    if not os.path.exists(path): return path
    base, ext = os.path.splitext(path)
    i = 2
    while True:
        new_path = f"{base}__v{i}{ext}"
        if not os.path.exists(new_path): return new_path
        i += 1

def extract_user_inputs(chat_text):
    """Extracts 'user' role content from JSON-like strings."""
    if pd.isna(chat_text) or str(chat_text).strip() in ["", "[]", "#VALUE!"]:
        return []
    txt = str(chat_text)
    pattern = r'"role"\s*:\s*"user"\s*,\s*"content"\s*:\s*"((?:\\.|[^"\\])*)"'
    matches = re.findall(pattern, txt)
    cleaned_matches = []
    for m in matches:
        out = m.replace(r'\n', '\n').replace(r'\t', '\t').replace(r'\"', '"').replace(r'\\', '\\')
        out = out.strip()
        if out: cleaned_matches.append(out)
    return cleaned_matches

def pick_col_value(row, cols_pref):
    """Returns the first non-empty value found."""
    for col in cols_pref:
        if col not in row.index: continue
        val = row[col]
        if pd.isna(val): continue
        val_str = str(val).strip()
        if val_str == "" or val_str == "#VALUE!": continue
        return val_str
    return None

def make_transcripts_one_lang(df, out_dir, k_values, lang):
    """Generates text files, keeping duplicates via versioning."""
    
    # Safety: Delete old folder to start fresh
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    
    meta_cols = [c for c in ["province", "district", "duration", "name"] if c in df.columns]
    count = 0
    
    print(f"\n--- Generating {lang.upper()} Transcripts ---")
    
    # Iterate through ALL rows (including duplicates)
    for idx, row in df.iterrows():
        person = row['name']
        person_safe = safe_filename(person)

        for k in k_values:
            lines = []

            # 1. Get Condition Code
            cond_col = f"case_{k}_condition"
            cond_code_raw = pick_col_value(row, [cond_col])
            
            # Check if this specific case has data (Chat or Condition)
            chat_col_check = f"custom_system_chat{k}_{lang}"
            chat_content = row.get(chat_col_check, "")
            
            has_condition = cond_code_raw and str(cond_code_raw).strip().upper() not in ["UNK", "NAN", ""]
            has_chat = not pd.isna(chat_content) and str(chat_content).strip() not in ["", "[]", "#VALUE!"]
            
            # If neither exists, skip this case
            if not has_condition and not has_chat:
                continue 

            if not has_condition: cond_code_raw = "UNK"
            
            cond_for_file = str(cond_code_raw)[:3].lower()
            condition_safe = safe_filename(cond_for_file)

            # 2. Extract Data
            user_msgs = []
            if chat_col_check in row.index:
                user_msgs = extract_user_inputs(row[chat_col_check])

            fields_map = {
                "Diagnosis": [f"patient_{k}_diagnosis_{lang}", f"patient_{k}_diagnosis_eng"],
                "Treatment": [f"patient_{k}_treatment_{lang}", f"patient_{k}_treatment_eng"],
                "Treatment_Post": [f"patient_{k}_treatment_post_{lang}", f"patient_{k}_treatment_post_eng"]
            }

            # 3. Build Text
            title = f"Transcript — {person}"
            lines.append(title)
            lines.append("=" * len(title))
            lines.append("")

            if meta_cols:
                for mc in meta_cols:
                    val = row[mc]
                    lines.append(f"{mc}: {val}")
                lines.append("")

            lines.append("User inputs:")
            lines.append("------------")
            if not user_msgs:
                lines.append("(No user messages found in chat.)")
                lines.append("")
            else:
                for i, msg in enumerate(user_msgs, 1):
                    lines.append(f"{i}.")
                    lines.append(msg)
                    lines.append("")

            lines.append("Other fields:")
            lines.append("------------")
            for label, cols in fields_map.items():
                val = pick_col_value(row, cols)
                if val:
                    lines.append(f"{label}:")
                    lines.append(val)
                    lines.append("")

            # 4. Save File (Handles duplicates automatically)
            filename = f"{condition_safe}__{person_safe}__case_{k}.txt"
            file_path_raw = os.path.join(out_dir, filename)
            
            # This function adds __v2 if the file already exists (duplicate user)
            final_path = make_unique_path(file_path_raw)
            
            with open(final_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
                
            count += 1

    print(f"Created: {count} files.")

def main():
    print(f"Loading {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: File not found at {INPUT_FILE}")
        return

    print(f"Initial Rows: {len(df)}")

    # ================================
    # RELAXED FILTERING logic
    # ================================
    # Keep row if ANY 'custom_system_*' column has valid data (not #VALUE! or empty)
    custom_cols = [c for c in df.columns if c.startswith("custom_system_")]
    
    def is_valid_cell(x):
        s = str(x).strip()
        return pd.notna(x) and s != "" and s != "#VALUE!" and s != "[]"

    # Row is valid if ANY custom_system column is valid
    mask_valid = df[custom_cols].apply(lambda row: any(is_valid_cell(x) for x in row), axis=1)
    df_clean = df[mask_valid].copy()

    print(f"Rows after removing completely empty/#VALUE! rows: {len(df_clean)}")
    print(f"Dropped {len(df) - len(df_clean)} rows (pure garbage).")
    
    # Note: We are NOT dropping duplicates by name.
    # Note: We are NOT filtering "test" or "009".
    
    print("-" * 30)
    print(f"PROCESSING COUNT: {len(df_clean)} rows")
    print("-" * 30)

    # Generate English
    make_transcripts_one_lang(df_clean, OUT_DIR_ENG, K_VALUES, "eng")

    # Generate Vietnamese
    make_transcripts_one_lang(df_clean, OUT_DIR_VIET, K_VALUES, "viet")

if __name__ == "__main__":
    main()