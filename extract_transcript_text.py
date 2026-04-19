"""Extract transcript text files from the source CSV for ENG and VIET runs."""

import os
import re
import shutil

import pandas as pd

from pipeline_config import INPUT_FILE, K_VALUES, TRANSCRIPTS_ENG_DIR, TRANSCRIPTS_VIET_DIR


def safe_filename(value):
    """Sanitize strings for file names."""
    if pd.isna(value):
        return "UNKNOWN"
    cleaned = str(value).strip()
    cleaned = re.sub(r'[\\/*?:"<>|]', "_", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned.strip("_")[:120]


def make_unique_path(path):
    """Avoid overwriting duplicates by appending __v2, __v3, etc."""
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    version = 2
    while True:
        candidate = f"{base}__v{version}{ext}"
        if not os.path.exists(candidate):
            return candidate
        version += 1


def is_valid_cell(value):
    """A valid value is non-empty and not an Excel placeholder/error marker."""
    if pd.isna(value):
        return False
    stripped = str(value).strip()
    return stripped not in {"", "#VALUE!", "[]"}


def pick_col_value(row, preferred_columns):
    """Return the first non-empty value found among candidate columns."""
    for column in preferred_columns:
        if column not in row.index:
            continue
        value = row[column]
        if pd.isna(value):
            continue
        value_str = str(value).strip()
        if value_str in {"", "#VALUE!"}:
            continue
        return value_str
    return None


def extract_user_inputs(chat_text):
    """Extract user-role content from JSON-like serialized chat text."""
    if pd.isna(chat_text) or str(chat_text).strip() in {"", "[]", "#VALUE!"}:
        return []

    text = str(chat_text)
    pattern = r'"role"\s*:\s*"user"\s*,\s*"content"\s*:\s*"((?:\\.|[^"\\])*)"'
    matches = re.findall(pattern, text)

    cleaned_messages = []
    for match in matches:
        parsed = (
            match.replace(r"\n", "\n")
            .replace(r"\t", "\t")
            .replace(r"\"", '"')
            .replace(r"\\", "\\")
            .strip()
        )
        if parsed:
            cleaned_messages.append(parsed)
    return cleaned_messages


def get_case_condition(row, case_number):
    cond_col = f"case_{case_number}_condition"
    return pick_col_value(row, [cond_col])


def get_chat_payload(row, case_number, lang):
    chat_column = f"custom_system_chat{case_number}_{lang}"
    chat_text = row.get(chat_column, "")
    has_chat = is_valid_cell(chat_text)
    return chat_column, chat_text, has_chat


def resolve_case_identity(row, case_number, lang):
    """Return (condition_code, chat_column) if case should be emitted, else None."""
    cond_code_raw = get_case_condition(row, case_number)
    chat_column, _, has_chat = get_chat_payload(row, case_number, lang)

    has_condition = bool(cond_code_raw) and str(cond_code_raw).strip().upper() not in {"UNK", "NAN", ""}
    if not has_condition and not has_chat:
        return None

    if not has_condition:
        cond_code_raw = "UNK"
    return cond_code_raw, chat_column


def build_transcript_lines(row, person, case_number, lang, chat_column):
    lines = []
    meta_cols = [column for column in ["province", "district", "duration", "name"] if column in row.index]
    user_messages = extract_user_inputs(row[chat_column]) if chat_column in row.index else []

    fields_map = {
        "Diagnosis": [f"patient_{case_number}_diagnosis_{lang}", f"patient_{case_number}_diagnosis_eng"],
        "Treatment": [f"patient_{case_number}_treatment_{lang}", f"patient_{case_number}_treatment_eng"],
        "Treatment_Post": [
            f"patient_{case_number}_treatment_post_{lang}",
            f"patient_{case_number}_treatment_post_eng",
        ],
    }

    title = f"Transcript — {person}"
    lines.append(title)
    lines.append("=" * len(title))
    lines.append("")

    if meta_cols:
        for meta_col in meta_cols:
            lines.append(f"{meta_col}: {row[meta_col]}")
        lines.append("")

    lines.append("User inputs:")
    lines.append("------------")
    if not user_messages:
        lines.append("(No user messages found in chat.)")
        lines.append("")
    else:
        for index, message in enumerate(user_messages, start=1):
            lines.append(f"{index}.")
            lines.append(message)
            lines.append("")

    lines.append("Other fields:")
    lines.append("------------")
    for label, columns in fields_map.items():
        value = pick_col_value(row, columns)
        if value:
            lines.append(f"{label}:")
            lines.append(value)
            lines.append("")

    return lines


def make_transcripts_one_lang(df, output_dir, lang):
    """Generate transcript text files for one language."""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    created_count = 0
    print(f"\n--- Generating {lang.upper()} Transcripts ---")

    for _, row in df.iterrows():
        person = row["name"]
        person_safe = safe_filename(person)

        for case_number in K_VALUES:
            case_identity = resolve_case_identity(row, case_number, lang)
            if case_identity is None:
                continue
            cond_code_raw, chat_column = case_identity

            condition_safe = safe_filename(str(cond_code_raw)[:3].lower())
            lines = build_transcript_lines(row, person, case_number, lang, chat_column)

            filename = f"{condition_safe}__{person_safe}__case_{case_number}.txt"
            destination = make_unique_path(os.path.join(output_dir, filename))
            with open(destination, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            created_count += 1

    print(f"Created: {created_count} files.")


def filter_valid_rows(df):
    """Keep rows where any custom_system_* cell has meaningful content."""
    custom_cols = [column for column in df.columns if column.startswith("custom_system_")]
    mask_valid = df[custom_cols].apply(lambda row: any(is_valid_cell(value) for value in row), axis=1)
    return df[mask_valid].copy()


def main():
    print(f"Loading {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: File not found at {INPUT_FILE}")
        return

    print(f"Initial Rows: {len(df)}")

    df_clean = filter_valid_rows(df)
    print(f"Rows after removing completely empty/#VALUE! rows: {len(df_clean)}")
    print(f"Dropped {len(df) - len(df_clean)} rows (pure garbage).")

    print("-" * 30)
    print(f"PROCESSING COUNT: {len(df_clean)} rows")
    print("-" * 30)

    make_transcripts_one_lang(df_clean, TRANSCRIPTS_ENG_DIR, "eng")
    make_transcripts_one_lang(df_clean, TRANSCRIPTS_VIET_DIR, "viet")


if __name__ == "__main__":
    main()
