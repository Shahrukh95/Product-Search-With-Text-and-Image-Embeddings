# Use the official NVIDIA Triton Server image
FROM nvcr.io/nvidia/tritonserver:24.01-py3

# Set the working directory
WORKDIR /workspace

# Install dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libcairo2-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install gdown to download from Google Drive
RUN pip install --no-cache-dir gdown

# Download model files
RUN gdown --folder https://drive.google.com/drive/folders/1E2D2ekxGa4uQ2mu9zrURKb3f8l85fFjS -O triton-server

# Install Python dependencies
RUN pip install --no-cache-dir -r triton-server/requirements.txt

# Expose flask and Triton ports
EXPOSE 5000 8000 8001 8002

# Start the Triton Server
CMD ["bash", "./triton-server/start.sh"]
