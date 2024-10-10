import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

if HUGGINGFACE_API_TOKEN is None:
    raise ValueError("HUGGINGFACE_API_TOKEN not found in the environment variables")

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")

# Initialize FastAPI app
app = FastAPI()

# Define request body
class TextGenerationRequest(BaseModel):
    prompt: str
    max_length: int = 200
    temperature: float = 0.7

# Define API endpoint
@app.post("/generate-text/")
async def generate_text(request: TextGenerationRequest):
    input_ids = tokenizer.encode(request.prompt, return_tensors="pt")

    # Generate text
    with torch.no_grad():
        output = model.generate(input_ids, max_length=request.max_length, num_beams=4, early_stopping=True)

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"generated_text": generated_text}

# Example usage
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)