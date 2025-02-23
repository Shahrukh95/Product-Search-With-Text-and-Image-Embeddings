# Use the official Ubuntu base image
# FROM python:3.13.2-slim
FROM nvcr.io/nvidia/tritonserver:25.01-trtllm-python-py3

WORKDIR /app
COPY . /app

# Install necessary dependencies
RUN apt-get update -y && apt-get install -y \
    build-essential curl wget git nano vim


# Expose Triton ports for API access
EXPOSE 8000 8001 8002

# Run Triton Server on container startup
CMD ["tritonserver", "--model-repository=/models"]