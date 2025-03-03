# Use official Python slim image
FROM python:3.13.2-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y curl nano build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "app.py"]
