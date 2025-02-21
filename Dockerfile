# Use the official Ubuntu base image
FROM python:3.13.2-slim

# Update the package list and install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y \
    build-essential curl wget git nano vim && \
    pip install transformers pillow jinja2 torch -y && \ 
    # Install Ollama
    # curl -fsSL https://ollama.com/install.sh | sh && \
    rm -rf /var/lib/apt/lists/**

    # pip install --upgrade ipywidgets
    # pip install --upgrade jupyter


WORKDIR /app
COPY . /app

# default command
CMD ["bash"]