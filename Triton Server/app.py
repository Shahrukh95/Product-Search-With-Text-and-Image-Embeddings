from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
import tritonclient.http as httpclient
import numpy as np
from transformers import AutoTokenizer, AutoImageProcessor
from PIL import Image
import io

app = FastAPI()

# Triton Server URL
TRITON_SERVER_URL = "localhost:8000"
client = httpclient.InferenceServerClient(url=TRITON_SERVER_URL)

# Model names
TEXT_MODEL_NAME = "UAE-Large-V1"
IMAGE_MODEL_NAME = "nomic-embed-vision"

# Load tokenizer and image processor
tokenizer = AutoTokenizer.from_pretrained("WhereIsAI/UAE-Large-V1")
image_processor = AutoImageProcessor.from_pretrained("nomic-ai/nomic-embed-vision-v1.5")

# Define request model for text inference
class TextInferenceRequest(BaseModel):
    texts: list[str]

@app.get("/health")
def health_check():
    try:
        # Check if Triton is alive
        if client.is_server_live():
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=503, detail="Triton server is not live yet")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Triton server check failed: {str(e)}")

@app.post("/infer_text")
def infer_text(texts: list[str]):
    if len(texts) > 128:
        raise HTTPException(status_code=400, detail="Batch size exceeds 128 texts")

    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="np")

    # Convert data types (Triton requires INT64)
    inputs["input_ids"] = inputs["input_ids"].astype(np.int64)
    inputs["attention_mask"] = inputs["attention_mask"].astype(np.int64)

    if "token_type_ids" not in inputs:
        inputs["token_type_ids"] = np.zeros_like(inputs["input_ids"])
    inputs["token_type_ids"] = inputs["token_type_ids"].astype(np.int64)

    # Create Triton inputs
    input_ids = httpclient.InferInput("input_ids", inputs["input_ids"].shape, "INT64")
    attention_mask = httpclient.InferInput("attention_mask", inputs["attention_mask"].shape, "INT64")
    token_type_ids = httpclient.InferInput("token_type_ids", inputs["token_type_ids"].shape, "INT64")

    # Set input data
    input_ids.set_data_from_numpy(inputs["input_ids"])
    attention_mask.set_data_from_numpy(inputs["attention_mask"])
    token_type_ids.set_data_from_numpy(inputs["token_type_ids"])

    # Define the output tensor
    outputs = httpclient.InferRequestedOutput("last_hidden_state")

    try:
        response = client.infer(
            model_name=TEXT_MODEL_NAME,
            inputs=[input_ids, attention_mask, token_type_ids],
            outputs=[outputs]
        )
        return {"result": response.as_numpy("last_hidden_state").tolist()}
    
    except Exception as e:
        return {"error": str(e)}


# Image Inference API
@app.post("/infer_image")
def infer_image(images: list[UploadFile] = File(...)):
    if len(images) > 64:
        raise HTTPException(status_code=400, detail="Batch size exceeds 64 images")

    image_list = []
    for image_file in images:
        # Read and process image
        image_bytes = image_file.file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Preprocess the image using Hugging Face processor
        inputs = image_processor(image, return_tensors="np")

        # Append to batch
        image_list.append(inputs["pixel_values"])

    # Stack into batch format
    batched_images = np.vstack(image_list).astype(np.float32)

    # Create Triton inputs
    triton_input = httpclient.InferInput("pixel_values", batched_images.shape, "FP32")
    triton_input.set_data_from_numpy(batched_images)

    outputs = httpclient.InferRequestedOutput("last_hidden_state")  # Ensure correct output name

    try:
        # Send request to Triton
        response = client.infer(
            model_name=IMAGE_MODEL_NAME,
            inputs=[triton_input],
            outputs=[outputs]
        )

        # Extract and normalize embeddings using NumPy
        img_embeddings = response.as_numpy("last_hidden_state")
        
        # Extract the first token (same as img_embeddings[:, 0])
        img_embeddings_first = img_embeddings[:, 0, :]
        
        # Normalize using NumPy
        norms = np.linalg.norm(img_embeddings_first, axis=1, keepdims=True)
        normalized_embeddings = img_embeddings_first / (norms + 1e-12)  # Avoid division by zero

        return {"image_embeddings": normalized_embeddings.tolist()}
    
    except Exception as e:
        return {"error": str(e)}
