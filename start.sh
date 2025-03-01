#!/bin/bash

cd Product-Search-With-Text-and-Image-Embeddings

# Start Triton Inference Server in the background
/opt/tritonserver/bin/tritonserver --model-repository=model_repository --http-port=8000 --allow-http=1 &

# Start FastAPI server on port 5000
uvicorn app:app --host 0.0.0.0 --port 5000
