import json

products = [
    {
        "id": "PROD-001",
        "title": "ZenBook Ultra 14",
        "description": "A lightweight 14-inch laptop with an OLED display, 16GB RAM, and 512GB SSD. Perfect for professionals on the go. Battery life up to 15 hours. Does not include a dedicated GPU.",
        "category": "Laptops",
        "price": 1299
    },
    {
        "id": "PROD-002",
        "title": "Titan X Gaming Laptop",
        "description": "Heavy-duty 17-inch gaming laptop featuring an RTX 4080 GPU, 32GB RAM, 1TB NVMe Gen4 SSD, and a 240Hz refresh rate screen. RGB backlit keyboard and advanced cooling system.",
        "category": "Laptops",
        "price": 2499
    },
    {
        "id": "PROD-003",
        "title": "NovaPhone Pro Max",
        "description": "The ultimate smartphone experience. Features a 6.7-inch AMOLED screen, 108MP triple camera setup, 5000mAh battery, and fast 120W charging. 5G ready.",
        "category": "Smartphones",
        "price": 1099
    },
    {
        "id": "PROD-004",
        "title": "EcoPhone Mini",
        "description": "A compact, eco-friendly smartphone made from recycled materials. 5.4-inch screen, dual 12MP cameras, perfect for one-handed use.",
        "category": "Smartphones",
        "price": 599
    },
    {
        "id": "PROD-005",
        "title": "SonicBuds Pro",
        "description": "True wireless earbuds with active noise cancellation (ANC), transparency mode, and spatial audio. Water-resistant and up to 30 hours of listening time with the charging case.",
        "category": "Accessories",
        "price": 199
    },
    {
        "id": "PROD-006",
        "title": "PowerBrick 100W",
        "description": "A high-capacity 20,000mAh power bank capable of charging laptops via USB-C at 100W. Includes 2 USB-C ports and 1 USB-A port.",
        "category": "Accessories",
        "price": 89
    }
]

if __name__ == "__main__":
    with open("product_catalog.json", "w") as f:
        json.dump(products, f, indent=4)
    print("product_catalog.json created successfully.")
