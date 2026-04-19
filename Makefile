# Preliminary Review Pipeline Makefile
# =====================================

PYTHON := python3

# Directories
DATA_DIR := data
ENG_DIR := transcripts_text_eng
VIET_DIR := transcripts_text_viet
RESULTS_DIR := results
RESULTS_VIET_DIR := results_viet

# Output
OUTPUT_FILE := aggregated_results.xlsx

# =====================================
# Main Targets
# =====================================

.PHONY: all all-viet extract analyze analyze-viet aggregate clean clean-all help

## Run the full English pipeline
all: extract analyze aggregate

## Run the full Vietnamese pipeline (assumes transcripts are extracted)
all-viet: analyze-viet

## Stage 1: Extract transcript text files from CSV
extract:
	@echo "=== Stage 1: Extracting transcripts ==="
	$(PYTHON) extract_transcript_text.py

## Stage 2: Analyze English transcripts with GPT-4o
analyze: | $(RESULTS_DIR)
	@echo "=== Stage 2: Analyzing English transcripts ==="
	$(PYTHON) analyze_transcripts.py

## Stage 2: Analyze Vietnamese transcripts with multiple models (ablation)
analyze-viet: | $(RESULTS_VIET_DIR)
	@echo "=== Stage 2: Analyzing Vietnamese transcripts (ablation) ==="
	$(PYTHON) analyze_transcripts_viet.py

## Stage 3: Aggregate JSON results to Excel (English)
aggregate:
	@echo "=== Stage 3: Aggregating English results ==="
	$(PYTHON) aggregate_results.py

# =====================================
# Directory Creation
# =====================================

$(RESULTS_DIR):
	@mkdir -p $(RESULTS_DIR)

$(RESULTS_VIET_DIR):
	@mkdir -p $(RESULTS_VIET_DIR)

# =====================================
# Cleaning
# =====================================

## Remove generated results (keeps transcripts)
clean:
	@echo "Removing results directories and output file..."
	rm -rf $(RESULTS_DIR) $(RESULTS_VIET_DIR)
	rm -f $(OUTPUT_FILE)

## Remove all generated files (transcripts + results)
clean-all: clean
	@echo "Removing transcript directories..."
	rm -rf $(ENG_DIR) $(VIET_DIR)

# =====================================
# Help
# =====================================

## Show this help message
help:
	@echo "Preliminary Review Pipeline"
	@echo "==========================="
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  all          Run full English pipeline (extract -> analyze -> aggregate)"
	@echo "  all-viet     Run full Vietnamese pipeline (analyze-viet)"
	@echo "  extract      Stage 1: Extract transcript text files from CSV"
	@echo "  analyze      Stage 2: Analyze English transcripts with GPT-4o"
	@echo "  analyze-viet Stage 2: Analyze Vietnamese transcripts with multiple models"
	@echo "  aggregate    Stage 3: Aggregate English JSON results to Excel"
	@echo "  clean        Remove results/ and output file"
	@echo "  clean-all    Remove all generated files (transcripts + results)"
	@echo "  help         Show this help message"
