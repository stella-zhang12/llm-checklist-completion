import os
import json
import importlib
import time
import random
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, BadRequestError, NotFoundError
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from pipeline_config import (
    ABLASTATS_VIET_FILE,
    MODELS_CONFIG,
    OPENAI_API_KEY_ENV,
    PROMPTS_PACKAGE,
    RESULTS_VIET_DIR,
    TOTAL_WORKERS,
    TRANSCRIPTS_VIET_DIR,
)

# 1. Setup Environment
load_dotenv()
client = OpenAI(api_key=os.getenv(OPENAI_API_KEY_ENV))

# --- CONFIGURATION CHANGES FOR VIETNAMESE RUN ---
INPUT_DIR = TRANSCRIPTS_VIET_DIR       # <--- New Input Folder
BASE_OUTPUT_DIR = RESULTS_VIET_DIR          # <--- New Output Folder
STATS_FILE = ABLASTATS_VIET_FILE   # <--- New Stats File

def get_prompt_template(prefix):
    try:
        module_name = f"{PROMPTS_PACKAGE}.{prefix}_prompt"
        module = importlib.import_module(module_name)
        return module.PROMPT_TEMPLATE
    except ModuleNotFoundError:
        return None
    except AttributeError:
        return None

def analyze_file(filename, prompt_template, model_id, output_path):
    """
    Processes a single file and returns the duration.
    """
    file_path = os.path.join(INPUT_DIR, filename)
    
    # Pre-check existence to save time
    if os.path.exists(output_path):
        return filename, True, "Skipped (Exists)", 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            transcript_text = f.read()
    except Exception as e:
        return filename, False, f"Read Error: {e}", 0

    # Insert Vietnamese text into English prompt
    prompt_content = prompt_template.replace(
        "{{INSERT_TRANSCRIPT_TEXT_HERE}}", 
        transcript_text
    )

    # Retry Logic
    max_retries = 5
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "You are a helpful medical data assistant."},
                    {"role": "user", "content": prompt_content}
                ],
                response_format={"type": "json_object"},
                temperature=0 
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            result_content = response.choices[0].message.content
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result_content)
                
            return filename, True, None, duration

        except RateLimitError:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
            
        except NotFoundError:
            return filename, False, f"Model '{model_id}' not found.", 0

        except BadRequestError as e:
            if "temperature" in str(e):
                try:
                    start_time = time.time()
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=[{"role": "user", "content": prompt_content}],
                        response_format={"type": "json_object"}
                    )
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(response.choices[0].message.content)
                    return filename, True, "Recovered (Default Temp)", duration
                except Exception as e2:
                    return filename, False, str(e2), 0
            return filename, False, f"API Error: {e}", 0
            
        except Exception as e:
            return filename, False, str(e), 0

    return filename, False, "Max retries exceeded", 0

def main():
    # 1. Gather all source files
    if not os.path.exists(INPUT_DIR):
        print(f"Error: Input directory '{INPUT_DIR}' not found.")
        return

    all_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")])
    base_tasks = []
    
    print(f"Scanning source files in {INPUT_DIR}...")
    for filename in all_files:
        try:
            prefix = filename.split("__")[0]
        except IndexError:
            continue
        template = get_prompt_template(prefix)
        if template:
            base_tasks.append((filename, template))

    if not base_tasks:
        print("No valid source tasks found.")
        return

    # 2. Build the Master Job List (FILTERED by existence)
    master_job_list = []
    skipped_count = 0
    
    print("Checking existing results to skip...")
    
    for folder_name, model_id in MODELS_CONFIG.items():
        out_dir = os.path.join(BASE_OUTPUT_DIR, folder_name)
        os.makedirs(out_dir, exist_ok=True)
        
        for filename, template in base_tasks:
            output_json_name = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(out_dir, output_json_name)
            
            if os.path.exists(output_path):
                skipped_count += 1
                continue 
            
            master_job_list.append({
                "model_name": folder_name,
                "model_id": model_id,
                "filename": filename,
                "template": template,
                "output_path": output_path
            })

    random.shuffle(master_job_list)

    total_possible = len(base_tasks) * len(MODELS_CONFIG)
    jobs_remaining = len(master_job_list)
    
    print(f"\n--- JOB SUMMARY (VIETNAMESE) ---")
    print(f"Total Possible Files: {total_possible}")
    print(f"Already Completed:    {skipped_count}")
    print(f"Remaining to Run:     {jobs_remaining}")
    print(f"Workers:              {TOTAL_WORKERS}")
    
    if jobs_remaining == 0:
        print("All jobs complete! Nothing to do.")
        return

    # 3. Initialize Progress Bars
    bars = {}
    timing_stats = {name: [] for name in MODELS_CONFIG.keys()}
    
    for i, model_name in enumerate(MODELS_CONFIG.keys()):
        model_specific_jobs = [j for j in master_job_list if j["model_name"] == model_name]
        bars[model_name] = tqdm(total=len(model_specific_jobs), desc=f"{model_name:<12}", position=i, unit="file", ncols=100)

    # 4. Execute
    global_start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=TOTAL_WORKERS) as executor:
        future_to_meta = {}
        for job in master_job_list:
            future = executor.submit(
                analyze_file, 
                job["filename"], 
                job["template"], 
                job["model_id"], 
                job["output_path"]
            )
            future_to_meta[future] = job

        for future in as_completed(future_to_meta):
            meta = future_to_meta[future]
            model_name = meta["model_name"]
            filename = meta["filename"]
            
            try:
                fname, success, msg, duration = future.result()
                
                bars[model_name].update(1)
                
                if success:
                    if duration > 0:
                        timing_stats[model_name].append(duration)
                else:
                    tqdm.write(f"[{model_name}] FAILED {filename}: {msg}")
            except Exception as e:
                tqdm.write(f"CRITICAL ERROR: {e}")

    global_end_time = time.time()

    for pbar in bars.values():
        pbar.close()

    # 5. Stats
    print("\nCalculating Statistics (New Run Only)...")
    final_metrics = {
        "run_wall_clock_time": round(global_end_time - global_start_time, 2),
        "models": {}
    }

    for model, times in timing_stats.items():
        count = len(times)
        if count > 0:
            avg_time = sum(times) / count
            total_model_time = sum(times)
            min_time = min(times)
            max_time = max(times)
        else:
            avg_time = 0
            total_model_time = 0
            min_time = 0
            max_time = 0

        final_metrics["models"][model] = {
            "newly_processed_count": count,
            "average_time": round(avg_time, 2),
            "min_time": round(min_time, 2),
            "max_time": round(max_time, 2),
            "total_time": round(total_model_time, 2)
        }
        
        print(f"[{model}] Processed: {count} | Avg: {avg_time:.2f}s")

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(final_metrics, f, indent=4)
    
    print(f"\nStats saved to {STATS_FILE}")

if __name__ == "__main__":
    main()
