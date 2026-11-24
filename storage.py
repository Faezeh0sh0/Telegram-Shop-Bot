import json

def save_products(product):
    with open("products.json", mode= "r+", encoding= "utf-8") as file:
        data = json.load(file)
        data["products"].append(product)
        file.seek(0)
        json.dump(data, file, indent = 4)
        file.truncate()

def load_products():
    with open("products.json", mode = "r", encoding= "utf-8") as file:
        data = json.load(file)
        return data["products"] #[0] بود باید یه کاری کنی که داخل main با for هر چی هست نمایش بدی

def edit_product(selected_product, edit_field):
    with open("products.json", mode = "r+", encoding= "utf-8") as file:
        data = json.load(file)
        for product in data['products']:
            if product["id"] == selected_product['id']:
                product[edit_field] = selected_product[edit_field]
                break
        file.seek(0)
        json.dump(data, file, indent = 4)
        file.truncate()

def delete_product(field_id):
    with open("products.json", mode = "r+", encoding= "utf-8") as file:
        data = json.load(file)
        count = -1
        for product in data["products"]:
            count +=1
            if product["id"] == field_id:
                data["products"].pop(count)
                break
        file.seek(0)
        json.dump(data, file, indent = 4)
        file.truncate()
