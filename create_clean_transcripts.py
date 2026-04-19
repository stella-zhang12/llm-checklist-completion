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
    Prevents overwriting. 
    NOTE: With the 'drop_duplicates' logic in main(), this should rarely be needed,
    but it's kept as a safety fallback.
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
    """Generates text files."""
    
    # 1. Safety Clean: Delete old folder to ensure no 'zombie' files remain
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    
    meta_cols = [c for c in ["province", "district", "duration", "name"] if c in df.columns]
    count = 0
    skipped_empty = 0
    
    print(f"\n--- Generating {lang.upper()} Transcripts ---")
    
    for idx, row in df.iterrows():
        person = row['name']
        person_safe = safe_filename(person)

        for k in k_values:
            lines = []

            # CHECK: Does this case exist?
            cond_col = f"case_{k}_condition"
            cond_code_raw = pick_col_value(row, [cond_col])
            
            # LOGIC: Check if case is valid (Condition code exists OR chat exists)
            # If condition is missing, check chat. If both missing -> SKIP.
            if not cond_code_raw or str(cond_code_raw).strip().upper() in ["UNK", "NAN", ""]:
                chat_col_check = f"custom_system_chat{k}_{lang}"
                chat_content = row.get(chat_col_check, "")
                
                # If no condition AND no chat data, this case didn't happen.
                if pd.isna(chat_content) or str(chat_content).strip() in ["", "[]", "#VALUE!"]:
                    skipped_empty += 1
                    continue 
                cond_code_raw = "UNK" # Chat exists but condition code missing

            cond_for_file = str(cond_code_raw)[:3].lower()
            condition_safe = safe_filename(cond_for_file)

            # Chat Extraction
            chat_col = f"custom_system_chat{k}_{lang}"
            user_msgs = []
            if chat_col in row.index:
                user_msgs = extract_user_inputs(row[chat_col])

            # Fields Map
            fields_map = {
                "Diagnosis": [f"patient_{k}_diagnosis_{lang}", f"patient_{k}_diagnosis_eng"],
                "Treatment": [f"patient_{k}_treatment_{lang}", f"patient_{k}_treatment_eng"],
                "Treatment_Post": [f"patient_{k}_treatment_post_{lang}", f"patient_{k}_treatment_post_eng"]
            }

            # Build Text Content
            title = f"Transcript — {person}"
            lines.append(title)
            lines.append("=" * len(title))
            lines.append("")

            # Metadata
            if meta_cols:
                for mc in meta_cols:
                    val = row[mc]
                    lines.append(f"{mc}: {val}")
                lines.append("")

            # User Chat
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

            # Other Fields
            lines.append("Other fields:")
            lines.append("------------")
            for label, cols in fields_map.items():
                val = pick_col_value(row, cols)
                if val:
                    lines.append(f"{label}:")
                    lines.append(val)
                    lines.append("")

            # Save
            filename = f"{condition_safe}__{person_safe}__case_{k}.txt"
            file_path_raw = os.path.join(out_dir, filename)
            final_path = make_unique_path(file_path_raw)
            
            with open(final_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
                
            count += 1

    print(f"Created: {count} files.")
    print(f"Skipped: {skipped_empty} empty cases.")

def main():
    print(f"Loading {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: File not found at {INPUT_FILE}")
        return

    print(f"Initial Rows: {len(df)}")

    # ================================
    # 1. CLEANING: Remove Duplicates (Smart)
    # ================================
    # Sort by length of text in case 1, so the "fullest" row comes first
    if 'custom_system_chat1_eng' in df.columns:
        df['chat_len'] = df['custom_system_chat1_eng'].astype(str).apply(len)
        df = df.sort_values('chat_len', ascending=False)
    
    # Drop duplicates by Name, keeping the one with most text
    df_clean = df.drop_duplicates(subset='name', keep='first').copy()
    print(f"Rows after removing duplicates: {len(df_clean)} (Dropped {len(df) - len(df_clean)})")

    # ================================
    # 2. FILTERING: 'Test' and '009'
    # ================================
    if 'name' in df_clean.columns:
        initial_clean_count = len(df_clean)
        
        # Remove 'test' (case insensitive)
        mask_test = df_clean['name'].astype(str).str.lower().str.contains("test")
        
        # Remove ending in '009' (strip whitespace first!)
        mask_009 = df_clean['name'].astype(str).str.strip().str.endswith("009")
        
        df_clean = df_clean[~mask_test & ~mask_009]
        
        print(f"Rows after filtering 'test' and '009': {len(df_clean)} (Dropped {initial_clean_count - len(df_clean)})")

    # ================================
    # 3. FILTERING: Excel Errors
    # ================================
    # If the first case chat is #VALUE!, the row is likely broken
    if 'custom_system_chat1_eng' in df_clean.columns:
        pre_err_count = len(df_clean)
        df_clean = df_clean[df_clean['custom_system_chat1_eng'].astype(str) != "#VALUE!"]
        if len(df_clean) < pre_err_count:
            print(f"Rows after removing #VALUE! errors: {len(df_clean)} (Dropped {pre_err_count - len(df_clean)})")

    print("-" * 30)
    print(f"FINAL CLEAN PROVIDER COUNT: {len(df_clean)}")
    print("-" * 30)

    # 4. Generate English Set
    make_transcripts_one_lang(df_clean, OUT_DIR_ENG, K_VALUES, "eng")

    # 5. Generate Vietnamese Set
    make_transcripts_one_lang(df_clean, OUT_DIR_VIET, K_VALUES, "viet")

if __name__ == "__main__":
    main()