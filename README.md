# Preliminary Review Pipeline

A pipeline for extracting, analyzing, and aggregating medical transcript data using LLM-based evaluation.

## Overview

This pipeline processes medical consultation transcripts through three stages:

1. **Extract** -- Parse raw data and generate individual transcript text files
2. **Analyze** -- Evaluate transcripts against clinical checklists using GPT-4o or multiple models (ablation)
3. **Aggregate** -- Combine JSON results into a single Excel file

Supports both English and Vietnamese transcripts with separate processing pipelines.

## Requirements

- Python 3.8+
- OpenAI API key (set in `.env` file)

### Python Dependencies

```bash
pip install pandas python-dotenv openai tqdm openpyxl
```

### Environment Setup

Create a `.env` file in this directory:

```
OPENAI_API_KEY=your_api_key_here
```

## Directory Structure

```
preliminary-review-pipeline/
├── data/                        # Input data (gitignored)
│   └── llm-data-baseline-1125-translated.xlsx - data.csv
├── transcripts_text_eng/        # Extracted English transcripts (gitignored)
├── transcripts_text_viet/       # Extracted Vietnamese transcripts (gitignored)
├── results/                     # English JSON analysis results (gitignored)
├── results_viet/                # Vietnamese JSON analysis results (gitignored)
│   ├── gpt-4.1/                 # Results for gpt-4o model
│   ├── gpt-4.1-mini/            # Results for gpt-4o-mini model
│   └── gpt-4.1-nano/            # Results for gpt-3.5-turbo model
├── prompts/                     # Prompt templates by condition
│   ├── __init__.py
│   └── pne_prompt.py           # Pneumonia evaluation checklist
├── extract_transcript_text.py   # Stage 1: Extract transcripts
├── analyze_transcripts.py       # Stage 2: English LLM analysis
├── analyze_transcripts_viet.py  # Stage 2: Vietnamese LLM analysis (ablation)
├── aggregate_results.py         # Stage 3: Combine English results
├── aggregated_results.xlsx      # English final output
├── ablation_stats_resume.json   # English analysis stats
├── ablation_stats_viet.json     # Vietnamese analysis stats
├── Makefile                     # Build automation
└── README.md
```

## Usage

### Run Full Pipelines

```bash
# Full English pipeline
make all

# Full Vietnamese pipeline (assumes transcripts are extracted)
make all-viet
```

### Run Individual Stages

```bash
# Stage 1: Extract transcript text files from CSV
make extract

# Stage 2: Analyze English transcripts with GPT-4o
make analyze

# Stage 2: Analyze Vietnamese transcripts with multiple models (ablation)
make analyze-viet

# Stage 3: Aggregate English JSON results to Excel
make aggregate
```

### Other Commands

```bash
# Remove generated files (keeps data/)
make clean

# Remove everything including extracted transcripts
make clean-all

# Show available commands
make help
```

## Pipeline Details

### Stage 1: Extract (`extract_transcript_text.py`)

- **Input**: `data/llm-data-baseline-1125-translated.xlsx - data.csv`
- **Output**: `transcripts_text_eng/` and `transcripts_text_viet/`

Parses the source CSV and generates individual text files for each patient case. Files are named using the pattern: `{condition}__{patient_name}__case_{k}.txt`

Filters out test records (names containing "test" or ending in "009").

### Stage 2: Analyze English (`analyze_transcripts.py`)

- **Input**: `transcripts_text_eng/*.txt`
- **Output**: `results/*.json`

For each transcript, the script:
1. Extracts the condition prefix from the filename (e.g., `pne`)
2. Loads the corresponding prompt template from `prompts/{prefix}_prompt.py`
3. Sends the transcript to GPT-4o for evaluation
4. Saves the structured JSON response

Skips files that already have results (incremental processing).

### Stage 2: Analyze Vietnamese (`analyze_transcripts_viet.py`)

- **Input**: `transcripts_text_viet/*.txt`
- **Output**: `results_viet/{model}/*.json`

Similar to English analysis, but:
- Processes Vietnamese transcripts
- Runs ablation testing across multiple models: gpt-4o, gpt-4o-mini, gpt-3.5-turbo
- Outputs results in subdirectories by model
- Generates timing statistics in `ablation_stats_viet.json`

Uses the same English prompt templates with Vietnamese text inserted.

### Stage 3: Aggregate (`aggregate_results.py`)

- **Input**: `results/*.json`
- **Output**: `aggregated_results.xlsx`

Combines all English JSON results into a single Excel file with:
- Metadata columns: Filename, Prefix, Patient_Name, Case_ID
- Variable columns: All checklist items from the evaluation

## Adding New Conditions

To add evaluation for a new condition (e.g., diabetes):

1. Create `prompts/dia_prompt.py` with a `PROMPT_TEMPLATE` variable
2. Ensure transcript filenames start with `dia__` prefix
3. Run `make analyze` or `make analyze-viet` -- new files will be processed automatically

## Notes

- The `.gitignore` excludes `data/`, `transcripts_text_*/`, and `results*/` to protect PII
- Analysis uses `temperature=0` for reproducible results
- Existing results are skipped -- delete `results/` or `results_viet/` to reprocess all files
- Vietnamese pipeline focuses on ablation testing; aggregation for Vietnamese results may require a separate script