#!/bin/bash

# Move to the Triton server directory
cd Product-Search-With-Text-and-Image-Embeddings

# Start Triton Inference Server in the background
/opt/tritonserver/bin/tritonserver \
  --model-repository=model_repository \
  --http-port=8000 --allow-http=1 > triton.log 2>&1 &

TRITON_PID=$!

echo "Waiting for Triton Server to be ready..."
while ! grep -q "Started HTTPService at" triton.log; do
    sleep 1
    if ! kill -0 $TRITON_PID 2>/dev/null; then
        echo "Triton Server failed to start. Exiting..."
        exit 1
    fi
done
echo "Triton Server is running!"

# Start FastAPI (Uvicorn) server
uvicorn app:app --host 0.0.0.0 --port 5000 &

API_PID=$!

# Auto-shutdown if idle for 10 seconds
IDLE_TIMEOUT=30
LOG_FILE="/tmp/server_activity.log"
touch $LOG_FILE

echo "Monitoring activity for auto-shutdown..."

while true; do
    # Check if either process has exited unexpectedly
    if ! kill -0 $TRITON_PID 2>/dev/null; then
        echo "Triton Server crashed! Stopping everything..."
        kill $API_PID 2>/dev/null
        wait $API_PID 2>/dev/null
        exit 1
    fi

    if ! kill -0 $API_PID 2>/dev/null; then
        echo "FastAPI Server crashed! Stopping everything..."
        kill $TRITON_PID 2>/dev/null
        wait $TRITON_PID 2>/dev/null
        exit 1
    fi

    # Auto-shutdown if no activity for $IDLE_TIMEOUT seconds
    LAST_MODIFIED=$(stat -c %Y "$LOG_FILE")
    CURRENT_TIME=$(date +%s)
    TIME_DIFF=$((CURRENT_TIME - LAST_MODIFIED))

    if [[ $TIME_DIFF -ge $IDLE_TIMEOUT ]]; then
        echo "No activity detected for $IDLE_TIMEOUT seconds. Shutting down..."
        kill $TRITON_PID $API_PID 2>/dev/null
        wait $TRITON_PID 2>/dev/null
        wait $API_PID 2>/dev/null
        echo "Shutdown complete. Exiting..."
        exit 0
    fi

    sleep 5
done
