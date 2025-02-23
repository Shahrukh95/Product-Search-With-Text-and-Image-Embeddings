from pymongo import MongoClient
import os

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["productDB"]  # Database Name
collection = db["products"]  # Collection Name

# Function to insert multiple products
def insert_products(product_list):
    collection.insert_many(product_list)

# Function to fetch all products
def get_all_products():
    return list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id
