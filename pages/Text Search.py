import streamlit as st
from pymongo import MongoClient
import math
import os

# Set Streamlit page layout to wide
st.set_page_config(page_title="Text Embeddings",layout="wide", page_icon="🛒")
st.title("🛒 Text Embeddings - CLIP Model")

# load the mongo uri from .env file
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@mongodb:27017/")
MONGO_URI = "mongodb://admin:password@mongodb:27017/"
DB_NAME = "productDB"
COLLECTION_NAME = "products"

# Connect to MongoDB
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def get_products(page, page_size=6, search_query=None):
    db = get_db()
    collection = db[COLLECTION_NAME]
    
    query = {"title": {"$regex": search_query, "$options": "i"}} if search_query else {}
    total_count = collection.count_documents(query)
    total_pages = math.ceil(total_count / page_size)
    
    products = list(
        collection.find(query).skip((page - 1) * page_size).limit(page_size)
    )
    
    return products, total_pages

# Pagination Setup
page = st.number_input("Page Number", min_value=1, value=1, step=1)

# Search Bar
search_query = st.text_input("Search for a product", "")
products, total_pages = get_products(page, search_query=search_query.strip())

# Pagination Controls
st.markdown(f"**Total Pages:** {total_pages}")

# Display Products
if not products:
    st.warning("No products found!")
else:
    cols = st.columns(3)  # 3 products per row
    for idx, product in enumerate(products):
        with cols[idx % 3]:
            st.image(product["imgUrl"], width=200)
            truncated_title = product["title"][:150] + "..." if len(product["title"]) > 150 else product["title"]
            st.subheader(truncated_title)
            st.write(f'**Price:** ${product["price"]}')
            st.write(f'**Category:** {product["category"]["name"]}')
            st.write(f"**Llava Generated Image Caption:** {product.get("product_description_ai_generated", "No description available.")}")
            st.markdown(f'[🔗 View Product]({product["productURL"]})', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)



