import gradio as gr
import faiss
import numpy as np
import requests
import os
from pymongo import MongoClient
from io import BytesIO

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@mongodb:27017")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["productDB"]
collection = db["products"]

# FAISS Index Paths
FAISS_INDEX_TEXT_PATH = "Embeddings/text-embeddings/faiss_index.bin"
FAISS_INDEX_IMG_PATH = "Embeddings/image_embeddings/faiss_index_images.bin"

# Load FAISS Indexes
index_text = faiss.read_index(FAISS_INDEX_TEXT_PATH)
index_images = faiss.read_index(FAISS_INDEX_IMG_PATH)

# API Endpoint for Inference
RUNPOD_API_ENDPOINT = "https://26oe7qh881svy7-5000.proxy.runpod.net/"  # Change this accordingly

def find_similar_text(query_text, k=5):
    response = requests.post(f"{RUNPOD_API_ENDPOINT}/infer_text", json=[query_text])
    query_embedding = np.array(response.json()['result'])
    query_embedding = np.mean(query_embedding, axis=1)
    
    distances, indices = index_text.search(query_embedding, k)
    
    results = []
    for idx, distance in zip(indices[0], distances[0]):
        product = collection.find_one({"text_embedding_index": int(idx)})  # Ensure int conversion
        
        if product:
            results.append({
                "Title": product.get("title", ""),
                "Llava Generated Image Description": product.get("product_description_ai_generated", ""),
                "Price ($)": product.get("price", ""),
                "Category": product.get("category", {}).get("name", ""),
                "Image": product.get("imgUrl", ""),
                "Product URL": product.get("productURL", ""),
                "Distance": round(float(distance), 4)
            })
    
    return [[res["Title"], res["Llava Generated Image Description"], res["Price ($)"], res["Category"], res["Image"], res["Product URL"], res["Distance"]] for res in results]

def find_similar_images(image, k=5):
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    files = [("images", ("query_image.jpg", image_bytes, "image/jpeg"))]
    
    response = requests.post(f"{RUNPOD_API_ENDPOINT}/infer_image", files=files)
    query_embedding = np.array(response.json()['image_embeddings'])
    
    distances, indices = index_images.search(query_embedding, k)
    
    results = []
    for idx, distance in zip(indices[0], distances[0]):
        product = collection.find_one({"image_embedding_index": int(idx)})  # Ensure int conversion
        
        if product:
            results.append({
                "Title": product.get("title", ""),
                "Llava Generated Image Description": product.get("product_description_ai_generated", ""),
                "Price ($)": product.get("price", ""),
                "Category": product.get("category", {}).get("name", ""),
                "Image": product.get("imgUrl", ""),
                "Product URL": product.get("productURL", ""),
                "Distance": round(float(distance), 4)
            })
    
    return [[res["Title"], res["Llava Generated Image Description"], res["Price ($)"], res["Category"], res["Image"], res["Product URL"], res["Distance"]] for res in results]

def text_search_interface(query):
    return find_similar_text(query)

def image_search_interface(image):
    return find_similar_images(image)

# Gradio UI
title = "🔍 Product Search using Embeddings"
description = "Search for similar products using text or image queries."

demo = gr.Interface(
    fn=text_search_interface,
    outputs=gr.Dataframe(headers=["Title", "Llava Generated Image Description", "Price ($)", "Category", "Image", "Product URL", "Distance"], interactive=False),
    inputs=gr.Textbox(label="Enter Product Query"),
    title=title,
    description=description,
)

demo2 = gr.Interface(
    fn=image_search_interface,
    outputs=gr.Dataframe(headers=["Title", "Llava Generated Image Description", "Price ($)", "Category", "Image", "Product URL", "Distance"], interactive=False),
    inputs=gr.Image(type="pil", label="Upload an Image"),
    title=title,
    description=description,
)

dashboard = gr.TabbedInterface([demo, demo2], ["Text Search", "Image Search"])

dashboard.launch(server_name="0.0.0.0", server_port=7860, debug=True, share=True)
