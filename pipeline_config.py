"""Shared configuration for the checklist completion pipeline."""

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

# Input dataset
INPUT_FILE = "data/llm-data-baseline-1125-translated.xlsx - data.csv"

# Transcript directories
TRANSCRIPTS_ENG_DIR = "transcripts_text_eng"
TRANSCRIPTS_VIET_DIR = "transcripts_text_viet"

# Result directories
RESULTS_ENG_DIR = "results"
RESULTS_VIET_DIR = "results_viet"

# Aggregated workbook outputs
AGGREGATED_ENG_OUTPUT = "aggregated_results.xlsx"
AGGREGATED_VIET_OUTPUT = "aggregated_results_viet.xlsx"

# Ablation/runtime stats
ABLASTATS_ENG_FILE = "ablation_stats_resume.json"
ABLASTATS_VIET_FILE = "ablation_stats_viet.json"

# Prompt package import path
PROMPTS_PACKAGE = "prompts"

# Models used by both ENG and VIET analysis
MODELS_CONFIG = {
    "gpt-4.1": "gpt-4.1",
    "gpt-4.1-mini": "gpt-4.1-mini",
    "gpt-4.1-nano": "gpt-4.1-nano",
}

TOTAL_WORKERS = 10

# Shared transcript generation config
K_VALUES = range(1, 6)
