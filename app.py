# import streamlit as st
# # from db import get_all_products
# # import pymongo
# from pymongo import MongoClient


# # Set Streamlit page layout to wide
# st.set_page_config(page_title="Product Dashboard",layout="wide", page_icon="🛒")

# st.title("🛒 Product Dashboard")



# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")  # Update with your connection string
# db = client["productDB"]  # Replace with your database name
# collection = db["products"]  # Replace with your collection name

# def get_products(page: int, limit: int = 6):
#     """Fetch products with pagination from MongoDB"""
#     skip_count = (page - 1) * limit  # Calculate how many to skip
    
#     products_cursor = collection.find({}, {"_id": 0}).skip(skip_count).limit(limit)  # Skip and limit
#     products = list(products_cursor)  # Convert cursor to list

#     return products

# def get_total_products():
#     """Get total number of products in the database"""
#     return collection.count_documents({})

# # Pagination settings
# PRODUCTS_PER_PAGE = 6


# # Store current page in session state
# if "current_page" not in st.session_state:
#     st.session_state.current_page = 1

# # Get total number of products
# total_products = get_total_products()
# total_pages = (total_products - 1) // PRODUCTS_PER_PAGE + 1

# # Fetch products for the current page
# products = get_products(st.session_state.current_page, PRODUCTS_PER_PAGE)



# # Display products in a three-column layout
# if products:
#     cols = st.columns(3)  # Create three columns
#     for index, product in enumerate(products):
#         with cols[index % 3]:  # Assign products to columns
#             st.subheader(product["title"])
#             st.image(product["imgUrl"], use_container_width=True)
#             st.write(f"**Price:** ${product['price']}")
#             st.write(f"**Ratings:** {product['ratings']['average']}⭐ ({product['ratings']['totalReviews']} reviews)")
#             st.write(f"**Category:** {product['category']['name']}")
#             st.markdown(f"[View Product]({product['productURL']})")
#             st.markdown("---")

# else:
#     st.warning("No products found in the database!")

# # Pagination controls at the bottom
# st.write(f"**Page {st.session_state.current_page} of {total_pages}**")

# col1, col2 = st.columns([1, 1])
# with col1:
#     if st.session_state.current_page > 1:
#         if st.button("⬅️ Previous"):
#             st.session_state.current_page -= 1
#             st.rerun()

# with col2:
#     if st.session_state.current_page < total_pages:
#         if st.button("Next ➡️"):
#             st.session_state.current_page += 1
#             st.rerun()






# # st.subheader(product["title"])
# #             st.image(product["imgUrl"], use_container_width=True)
# #             st.write(f"**Price:** ${product['price']}")
# #             st.write(f"**Ratings:** {product['ratings']['average']}")
# #             # ⭐ ({product['ratings']['totalReviews']} reviews)
# #             st.write(f"**Category:** {product['category']['name']}")
# #             # st.write(f"**Best Seller:** {'Yes' if product['isBestSeller'] else 'No'}")
# #             # st.write(f"**Bought in Last Month:** {product['boughtInLastMonth']} units")
# #             st.markdown(f"[View Product]({product['productURL']})")
# #             st.markdown("---")






import streamlit as st
import pymongo
import os
import math
import urllib

DB_NAME = "productDB"
COLLECTION_NAME = "products"

# Connect to MongoDB
@st.cache_resource
def get_db_connection():
    client = pymongo.MongoClient(MONGO_URI)
    return client[DB_NAME]

db = get_db_connection()
collection = db[COLLECTION_NAME]

# Pagination Settings
PAGE_SIZE = 10  # Number of items per page

# Get total number of documents
total_documents = collection.count_documents({})
total_pages = math.ceil(total_documents / PAGE_SIZE)

# Streamlit UI
st.title("Paginated Product List from MongoDB")

# Page selector
page = st.number_input("Select Page", min_value=1, max_value=total_pages, value=1, step=1)

# Fetch paginated results
def get_paginated_results(page, page_size):
    skip = (page - 1) * page_size
    results = collection.find({}, {"_id": 0}).skip(skip).limit(page_size)
    return list(results)

# Display products
products = get_paginated_results(page, PAGE_SIZE)

for product in products:
    st.subheader(product["title"])
    st.image(product["imgUrl"], width=150)
    st.write(f"**Price:** ${product['price']}")
    st.write(f"**Category:** {product['category']['name']}")
    st.write(f"**Rating:** {product['ratings']['average']} ⭐")
    st.markdown(f"[View Product]({product['productURL']})")

# Show pagination info
st.write(f"Page {page} of {total_pages}")
