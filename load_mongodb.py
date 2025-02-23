import pandas as pd
from db import insert_products

csv_file = "dataset/textual/filtered/selected_products.csv"
df = pd.read_csv(csv_file)

products = []

for _, row in df.iterrows():
    product = {
        "asin": row["asin"],
        "title": row["title"],
        "imgUrl": row["imgUrl"],
        "productURL": row["productURL"],
        "ratings": {
            "average": float(row["stars"]),
            # "totalReviews": int(row["reviews"])
        },
        "price": float(row["price"]),
        "category": {
            "id": row["category_id"],
            "name": row["category_name"]
        },
        # "isBestSeller": bool(row["isBestSeller"]),
        # "boughtInLastMonth": int(row["boughtInLastMonth"]),
        "product_description_ai_generated": "Coming Soon!"
    }
    products.append(product)

# Insert data into MongoDB
insert_products(products)



print(f"{len(products)} products inserted successfully!")
