import requests
from bs4 import BeautifulSoup

BASE_URL = "https://scrapeme.live/shop/"

response = requests.get(BASE_URL, timeout=30)

page_content = BeautifulSoup(response.text, "html.parser")
all_product_cards = page_content.find_all("li", {"class" : "type-product"})

product_links = []
for product in all_product_cards:
    link = product.find ("a", {"class" : "woocommerce-loop-product__link"})
    product_links.append(link)

for link in product_links:
    print(link["href"])
    print("=============================")
