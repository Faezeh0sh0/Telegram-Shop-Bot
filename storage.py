import json

def save_products(product):
    with open("products.json", mode= "w", encoding= "utf-8") as file:
        json.dump(product, file, indent = 2)