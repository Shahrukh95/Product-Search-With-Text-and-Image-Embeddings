#!/bin/bash

# Start Triton Inference Server in the background
/opt/tritonserver/bin/tritonserver \
  --model-repository=/workspace/Product-Search-With-Text-and-Image-Embeddings/model_repository \
  --http-port=8000 --allow-http=1 &

# Wait for Triton to be ready by checking logs
while ! grep -q "Started HTTPService at" <(timeout 30 tail -f /dev/null 2>&1); do
  sleep 1
done

echo "Triton Server is ready. Starting Flask server..."

# Start Flask server in the background
uvicorn app:app --host 0.0.0.0 --port 5000 &

echo "Both servers are running. Press Ctrl+C to stop."

# Keep the script running
wait
