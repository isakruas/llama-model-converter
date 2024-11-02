import http.server
import json
import socketserver
import textwrap

import torch
from transformers import LlamaForCausalLM, PreTrainedTokenizerFast
from transformers.generation.configuration_utils import GenerationConfig

# Model
LLAMA_MODEL = "Llama3.2-1B-Instruct"

# Load the tokenizer and Llama model
tokenizer = PreTrainedTokenizerFast.from_pretrained(
    f"models/transformers/{LLAMA_MODEL}"
)
model = LlamaForCausalLM.from_pretrained(f"models/transformers/{LLAMA_MODEL}")

# Model configurations
try:
    if torch.cuda.is_available():
        model = model.to("cuda")
except torch.OutOfMemoryError:
    model = model.to("cpu")

model.generation_config.pad_token_id = tokenizer.pad_token_id

# Generation settings
generation_config = GenerationConfig(
    max_new_tokens=128 * 10**2,
    max_time=120.0,
    stop_strings=["<|end_of_text|>", "<|eot_id|>", "<|eom_id|>"],
)


def generate_text(prompt):
    """Generates text based on the provided prompt using the Llama model.

    Args:
        prompt (str): The input text to guide the generation process.

    Returns:
        str: The generated text.
    """
    model.generation_config.pad_token_id = tokenizer.pad_token_id
    inputs = tokenizer(textwrap.dedent(prompt).strip(), return_tensors="pt").to(
        model.device
    )
    outputs = model.generate(
        **inputs, generation_config=generation_config, tokenizer=tokenizer
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
    return textwrap.dedent(generated_text).strip().replace("<|begin_of_text|>", "")


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for generating text based on prompts."""

    def do_POST(self):
        """Handles POST requests to generate text from a prompt.

        Reads the JSON body, extracts the prompt, generates text,
        and sends back the generated text in JSON format.
        """
        # Read the length of the content
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        # Load data from JSON
        data = json.loads(post_data)
        prompt = data.get("prompt", "")

        # Generate text based on the prompt
        generated_text = generate_text(prompt)

        # Prepare the response
        response = {"generated_text": generated_text}

        try:
            # Send the response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        except BrokenPipeError:
            pass


# Define the server port
PORT = 5000

# Create and start the server with a timeout of 120 seconds
try:
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        httpd.timeout = 120  # Set timeout to 120 seconds
        print(f"Server running on port {PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped by user.")
