import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://scrapeme.live/shop/"
response = requests.get (BASE_URL, timeout= 29)

page_content = BeautifulSoup (response.text, "html.parser")
all_cards = page_content.find_all ("li", {"class" : "type-product"})

products = []

for card in all_cards:
    name = card.find ("h2").get_text(strip=True)
    price = card.find ("span", {"class" : "price"}).get_text(strip=True)
    
    products.append({
        "name" : name,
        "price" : price
    })

with open ("names-prices.json", "w", encoding="utf-8") as file:
     json.dump(products, file, indent=4, ensure_ascii=False)


