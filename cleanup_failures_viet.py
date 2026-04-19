import os
import json
import importlib
import time
from dotenv import load_dotenv
from openai import OpenAI
from pipeline_config import (
    MODELS_CONFIG,
    OPENAI_API_KEY_ENV,
    PROMPTS_PACKAGE,
    RESULTS_VIET_DIR,
    TRANSCRIPTS_VIET_DIR,
)

# 1. Setup
load_dotenv()
client = OpenAI(api_key=os.getenv(OPENAI_API_KEY_ENV))

# --- VIETNAMESE CONFIGURATION ---
INPUT_DIR = TRANSCRIPTS_VIET_DIR
BASE_OUTPUT_DIR = RESULTS_VIET_DIR

def get_prompt_template(prefix):
    try:
        module = importlib.import_module(f"{PROMPTS_PACKAGE}.{prefix}_prompt")
        return module.PROMPT_TEMPLATE
    except:
        return None

def process_single_file(filename, model_folder, model_id):
    """
    Tries to process a file with verbose error logging.
    """
    prefix = filename.split("__")[0]
    template = get_prompt_template(prefix)
    if not template: 
        print(f"⚠️ Skipping {filename}: No prompt template found for prefix '{prefix}'")
        return
    
    file_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(BASE_OUTPUT_DIR, model_folder, os.path.splitext(filename)[0] + ".json")

    # Read
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        # --- EMPTY FILE CHECK ---
        if not text.strip():
            print(f"⚠️ Skipping {filename}: File is empty.")
            return
            
    except Exception as e:
        print(f"❌ Read Error for {filename}: {e}")
        return
    
    prompt = template.replace("{{INSERT_TRANSCRIPT_TEXT_HERE}}", text)

    print(f"🔄 Retrying {filename} on {model_id}...")

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are a helpful medical data assistant."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        # Save
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.choices[0].message.content)
        print(f"✅ SUCCESS: {filename}")
        
    except Exception as e:
        print(f"❌ PERMANENT FAIL: {e}")

def main():
    print("--- SCANNING FOR MISSING VIETNAMESE FILES ---")
    missing_tasks = []

    # 1. Find what is missing
    if not os.path.exists(INPUT_DIR):
        print(f"Error: Directory '{INPUT_DIR}' not found.")
        return

    all_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]
    
    for folder, model_id in MODELS_CONFIG.items():
        out_dir = os.path.join(BASE_OUTPUT_DIR, folder)
        # Ensure output directory exists (in case the main run didn't make it)
        os.makedirs(out_dir, exist_ok=True)
        
        for fname in all_files:
            expected_json = os.path.splitext(fname)[0] + ".json"
            if not os.path.exists(os.path.join(out_dir, expected_json)):
                missing_tasks.append((fname, folder, model_id))

    if not missing_tasks:
        print("🎉 All files are accounted for! No clean-up needed.")
        return

    print(f"Found {len(missing_tasks)} missing files. Processing sequentially...")
    
    # 2. Run them one by one
    for fname, folder, mid in missing_tasks:
        process_single_file(fname, folder, mid)
        time.sleep(1) # Polite pause to reset rate limits

if __name__ == "__main__":
    main()
