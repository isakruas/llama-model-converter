# Default directories and parameters; can be overridden from the command line
LLAMA_MODEL ?= Llama3.2-1B-Instruct
INPUT_DIR ?= models/meta-llama/$(LLAMA_MODEL)
OUTPUT_DIR ?= models/transformers/$(LLAMA_MODEL)
MODEL_SIZE ?= 1B
LLAMA_VERSION ?= 3.2

# Virtual environment directory
VENV_DIR := venv

# Set up virtual environment and install required packages
setup_environment:
	@echo "Setting up virtual environment..."
	@if [ ! -d "$(VENV_DIR)" ]; then python3 -m venv $(VENV_DIR); fi
	@echo "Installing required packages..."
	$(VENV_DIR)/bin/pip install -q 'transformers>=4.46.1'
	$(VENV_DIR)/bin/pip install -q 'torch>=2.5.1'
	$(VENV_DIR)/bin/pip install -q 'tiktoken>=0.8.0'
	$(VENV_DIR)/bin/pip install -q 'blobfile>=3.0.0'
	$(VENV_DIR)/bin/pip install -q 'accelerate>=1.1.0'
	@echo "Environment setup complete."

# Convert Llama weights to Hugging Face format
convert_model: setup_environment
	@echo "Converting Llama model weights..."
	$(VENV_DIR)/bin/python convert_llama_weights_to_hf.py \
		--input_dir $(INPUT_DIR) \
		--model_size $(MODEL_SIZE) \
		--llama_version $(LLAMA_VERSION) \
		--output_dir $(OUTPUT_DIR)
	@echo "Model conversion complete."

# Run the main Python application
run: setup_environment
	@echo "Running run_model.py..."
	$(VENV_DIR)/bin/python run_model.py

# Test the application with a POST request using curl
test:
	@echo "Running test with curl..."
	curl -X POST http://127.0.0.1:5000 \
	-H "Content-Type: application/json" \
	-d '{"prompt": "<|start_header_id|>system<|end_header_id|>\n\nEnvironment: ipython\n\n<|eot_id|>\n\n<|start_header_id|>user<|end_header_id|>\n\nWrite code to check if a number is prime, use that to see if the number 7 is prime\n\n<|eot_id|>"}' \
	--max-time 120 | jq --indent 4 .

# Default target to set up the environment and convert the model
install: convert_model

# Output the link to the documentation
doc:
	@echo "Link to documentation: https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/"
	@echo "Link to download: https://www.llama.com/llama-downloads/"

# Set the default target to call 'doc'
.DEFAULT_GOAL := doc
