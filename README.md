# Llama Model Converter

This project allows you to convert Llama model weights to the Hugging Face format, making it easier to work with Llama models in various applications.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9 or higher
- pip (Python package installer)
- curl (for testing the application)

## Getting Started

### 1. Download the Llama Model

Visit the Meta website to download the desired Llama model. Save the model files in the `models/meta-llama` directory. Your directory structure should look something like this:

```
project-root/
├── convert_llama_weights_to_hf.py
├── LICENSE.txt
├── llama_model_list.txt
├── Makefile
├── models
│   ├── meta-llama
│   │   ├── Llama3.2-3B-Instruct  # example model directory
│   │   │   ├── checklist.chk
│   │   │   ├── consolidated.00.pth
│   │   │   ├── params.json
│   │   │   ├── tokenizer.model
│   └── transformers
└── ...
```

### 2. Set the Model Name

Open the `Makefile` and replace the `LLAMA_MODEL` variable with the name of the model you downloaded. For example:

```
LLAMA_MODEL ?= Llama3.2-1B-Instruct
MODEL_SIZE ?= 1B
LLAMA_VERSION ?= 3.2
```

### 3. Install Required Packages and Convert the Model

Run the following command in your terminal to set up the environment and convert the model:

```
make install
```

This command will create a virtual environment, install the required packages, and convert the Llama model weights.

### 4. Run the Model

To run the model, execute:

```
make run
```

### 5. Test the Application

You can test the application with a sample POST request using curl:

```
make test
```

### Documentation

For more information on the model and prompt formats, visit:

- [Llama Documentation](https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/)
- [Llama Downloads](https://www.llama.com/llama-downloads/)

## License

This project uses the Llama 3.2 model, which is licensed under the Llama 3.2 Community License, Copyright © Meta Platforms, Inc. All Rights Reserved.

You can find the terms of the Llama 3.2 Community License at: [Llama 3.2 Community License](https://www.llama.com/license)

This project also includes code and resources that are licensed under the Apache License, Version 2.0, January 2004.

You can find the terms of the Apache License at: [Apache License 2.0](LICENSE.txt)