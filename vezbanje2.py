import requests
from bs4 import BeautifulSoup

BASE_URL = "https://scrapeme.live/shop/"
response = requests.get(BASE_URL, timeout=29)

page_content = BeautifulSoup(response.text, "html.parser")
all_cards = page_content.find_all("li", {"class": "type-product"})

all_articles_links = []

for card in all_cards:
    name = card.find("h2").get_text(strip=True)
    price_text = card.find("span", {"class": "price"}).get_text(strip=True)

    price = float(price_text.replace("£", ""))

    link = card.find("a").get("href")
    all_articles_links.append(link)

    if price > 50:
        print(name, "-", price, "£")

for link in all_articles_links:
    print(link)
 

for link in all_articles_links:
    response = requests.get(link, timeout=28)

    articles_content = BeautifulSoup (response.text, "html.parser")
    tags = articles_content.find("span", {"class": "tagged_as"})

    print(tags.get_text(strip=True))