# Use the official Ubuntu base image
FROM python:3.13.2-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y curl nano build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variables
ENV MONGO_URI=mongodb://admin:password@mongodb:27017/

# CMD ["streamlit", "run", "app.py"]
CMD ["tail", "-f", "/dev/null"]