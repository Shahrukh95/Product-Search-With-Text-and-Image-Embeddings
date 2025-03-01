# Use the official NVIDIA Triton Server image
FROM nvcr.io/nvidia/tritonserver:24.01-py3

# Set working directory inside the container
WORKDIR /workspace

# Install dependencies first
RUN apt-get update && apt-get install -y \
    pkg-config \
    libcairo2-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy model files first
COPY model_repository /workspace/model_repository

# Copy requirements separately to cache dependencies
COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy code files (avoids rebuilding if model_repository is unchanged)
COPY . /workspace

# Expose Flask (5000) and Triton ports (8000, 8001, 8002)
EXPOSE 5000 8000 8001 8002

# Start Triton Server with the model repository
CMD ["tritonserver", "--model-repository=/workspace/model_repository", "--allow-http", "--allow-grpc", "--http-port=8000", "--grpc-port=8001"]
