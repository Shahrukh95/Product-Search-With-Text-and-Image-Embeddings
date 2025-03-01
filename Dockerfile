# Use the official NVIDIA Triton Server image
FROM nvcr.io/nvidia/tritonserver:24.01-py3

# Set the working directory
WORKDIR /workspace

# Install dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libcairo2-dev \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install gdown to download from Google Drive
RUN pip install --no-cache-dir gdown

# Clone the correct branch of the repository
RUN git clone --single-branch --branch endpoint-creation \
    https://github.com/Shahrukh95/Product-Search-With-Text-and-Image-Embeddings.git

# Change the working directory to the cloned repository
WORKDIR /workspace/Product-Search-With-Text-and-Image-Embeddings

# Download model files into "model_repository" inside the repo folder
RUN gdown --folder https://drive.google.com/drive/folders/1E2D2ekxGa4uQ2mu9zrURKb3f8l85fFjS -O model_repository

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure start.sh is executable
RUN chmod +x start.sh

# Expose Flask (5000) and Triton ports (8000, 8001, 8002)
EXPOSE 5000 8000 8001 8002

# Start Triton Server
CMD ["bash", "start.sh"]
