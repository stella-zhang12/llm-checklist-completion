"""Shared analysis engine for English and Vietnamese transcript runs."""

import importlib
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv
from openai import BadRequestError, NotFoundError, OpenAI, RateLimitError
from tqdm import tqdm

from env_utils import get_openai_api_key


def _get_prompt_template(prefix, prompts_package):
    try:
        module_name = f"{prompts_package}.{prefix}_prompt"
        module = importlib.import_module(module_name)
        return module.PROMPT_TEMPLATE
    except (ModuleNotFoundError, AttributeError):
        return None


def _analyze_file(input_dir, client, filename, prompt_template, model_id, output_path):
    """Process a single transcript file for one model and return status metadata."""
    file_path = os.path.join(input_dir, filename)

    if os.path.exists(output_path):
        return filename, True, "Skipped (Exists)", 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            transcript_text = f.read()
    except Exception as exc:
        return filename, False, f"Read Error: {exc}", 0

    prompt_content = prompt_template.replace(
        "{{INSERT_TRANSCRIPT_TEXT_HERE}}",
        transcript_text,
    )

    max_retries = 5
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "You are a helpful medical data assistant."},
                    {"role": "user", "content": prompt_content},
                ],
                response_format={"type": "json_object"},
                temperature=0,
            )
            end_time = time.time()
            duration = end_time - start_time

            result_content = response.choices[0].message.content
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result_content)

            return filename, True, None, duration
        except RateLimitError:
            wait_time = (2**attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
        except NotFoundError:
            return filename, False, f"Model '{model_id}' not found.", 0
        except BadRequestError as exc:
            if "temperature" in str(exc):
                try:
                    start_time = time.time()
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=[{"role": "user", "content": prompt_content}],
                        response_format={"type": "json_object"},
                    )
                    end_time = time.time()
                    duration = end_time - start_time
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(response.choices[0].message.content)
                    return filename, True, "Recovered (Default Temp)", duration
                except Exception as nested_exc:
                    return filename, False, str(nested_exc), 0
            return filename, False, f"API Error: {exc}", 0
        except Exception as exc:
            return filename, False, str(exc), 0

    return filename, False, "Max retries exceeded", 0


def run_analysis(
    *,
    input_dir,
    output_dir,
    stats_file,
    models_config,
    total_workers,
    prompts_package,
    scan_message,
    job_summary_title,
    require_input_dir=False,
):
    """Run the shared transcript analysis flow."""
    load_dotenv()
    client = OpenAI(api_key=get_openai_api_key())

    if require_input_dir and not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        return

    all_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".txt")])
    base_tasks = []

    print(scan_message.format(input_dir=input_dir))
    for filename in all_files:
        try:
            prefix = filename.split("__")[0]
        except IndexError:
            continue
        template = _get_prompt_template(prefix, prompts_package)
        if template:
            base_tasks.append((filename, template))

    if not base_tasks:
        print("No valid source tasks found.")
        return

    master_job_list = []
    skipped_count = 0

    print("Checking existing results to skip...")
    for folder_name, model_id in models_config.items():
        model_output_dir = os.path.join(output_dir, folder_name)
        os.makedirs(model_output_dir, exist_ok=True)

        for filename, template in base_tasks:
            output_json_name = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(model_output_dir, output_json_name)

            if os.path.exists(output_path):
                skipped_count += 1
                continue

            master_job_list.append(
                {
                    "model_name": folder_name,
                    "model_id": model_id,
                    "filename": filename,
                    "template": template,
                    "output_path": output_path,
                }
            )

    random.shuffle(master_job_list)

    total_possible = len(base_tasks) * len(models_config)
    jobs_remaining = len(master_job_list)

    print(f"\n{job_summary_title}")
    print(f"Total Possible Files: {total_possible}")
    print(f"Already Completed:    {skipped_count}")
    print(f"Remaining to Run:     {jobs_remaining}")
    print(f"Workers:              {total_workers}")

    if jobs_remaining == 0:
        print("All jobs complete! Nothing to do.")
        return

    bars = {}
    timing_stats = {name: [] for name in models_config.keys()}

    for idx, model_name in enumerate(models_config.keys()):
        model_specific_jobs = [j for j in master_job_list if j["model_name"] == model_name]
        bars[model_name] = tqdm(
            total=len(model_specific_jobs),
            desc=f"{model_name:<12}",
            position=idx,
            unit="file",
            ncols=100,
        )

    global_start_time = time.time()
    with ThreadPoolExecutor(max_workers=total_workers) as executor:
        future_to_meta = {}
        for job in master_job_list:
            future = executor.submit(
                _analyze_file,
                input_dir,
                client,
                job["filename"],
                job["template"],
                job["model_id"],
                job["output_path"],
            )
            future_to_meta[future] = job

        for future in as_completed(future_to_meta):
            meta = future_to_meta[future]
            model_name = meta["model_name"]
            filename = meta["filename"]
            try:
                _, success, msg, duration = future.result()
                bars[model_name].update(1)
                if success:
                    if duration > 0:
                        timing_stats[model_name].append(duration)
                else:
                    tqdm.write(f"[{model_name}] FAILED {filename}: {msg}")
            except Exception as exc:
                tqdm.write(f"CRITICAL ERROR: {exc}")

    global_end_time = time.time()

    for progress_bar in bars.values():
        progress_bar.close()

    print("\nCalculating Statistics (New Run Only)...")
    final_metrics = {
        "run_wall_clock_time": round(global_end_time - global_start_time, 2),
        "models": {},
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
            "total_time": round(total_model_time, 2),
        }
        print(f"[{model}] Processed: {count} | Avg: {avg_time:.2f}s")

    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(final_metrics, f, indent=4)

    print(f"\nStats saved to {stats_file}")
