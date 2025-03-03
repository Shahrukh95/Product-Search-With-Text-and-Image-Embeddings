import pandas as pd
from db import insert_products

# Load product data
csv_file = "dataset/textual/complete/final_products.csv"
df = pd.read_csv(csv_file)

# Load embeddings
text_embeddings_csv = "Embeddings/text-embeddings/embeddings.csv"
image_embeddings_csv = "Embeddings/image_embeddings/image_embeddings.csv"

df_text_embeddings = pd.read_csv(text_embeddings_csv)
df_image_embeddings = pd.read_csv(image_embeddings_csv)

# Find valid indices (both text and image must exist)
valid_text_indices = set(df_text_embeddings.index)
valid_image_indices = set(df_image_embeddings.index)
valid_indices = valid_text_indices & valid_image_indices  # Keep only common indices

products = []

for idx, row in df.iterrows():
    # Skip if either text or image embedding is missing
    if idx not in valid_indices:
        print(f"Skipping product at index {idx} due to missing embedding.")
        continue

    product = {
        "text_embedding_index": idx,   # Store FAISS text index
        "image_embedding_index": idx,  # Store FAISS image index
        "asin": row["asin"],
        "title": row["title"],
        "imgUrl": row["imgUrl"],
        "productURL": row["productURL"],
        "price": float(row["price"]),
        "category": {
            "id": row["category_id"],
            "name": row["category_name"]
        },
        "product_description_ai_generated": row["llava_generated_image_caption"],
    }
    products.append(product)

# Insert data into MongoDB
insert_products(products)

print(f"{len(products)} valid products inserted successfully!")
