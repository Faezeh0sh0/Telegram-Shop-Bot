import json

def save_products(product):
    with open("products.json", mode= "r+", encoding= "utf-8") as file:
        data = json.load(file)
        data["products"].append(product)
        file.seek(0)
        json.dump(data, file, indent = 4)

def load_products():
    with open("products.json", mode = "r", encoding= "utf-8") as file:
        data = json.load(file)
        return data["products"][0]