import requests
import json
from bs4 import BeautifulSoup

BASE_URL = ('https://webscraper.io/test-sites/pagination?page=1')
current_url = BASE_URL

all_products = []
all_links = []
while current_url:
    response = requests.get(current_url, timeout=30)
    bs = BeautifulSoup(response.text, 'html.parser')
    cards = bs.find_all("div",{'class': 'col-md-4'})
    print("Acquiring links...")


    for card in cards:
        name = card.find('h3').get_text(strip=True)
        price = card.find('span', {'itemprop': 'price'}).get_text(strip=True)

        card_dict = {
            "name": name,
            "price": price,
        }
        all_products.append(card_dict)


   
    for card in cards:
        link = card.find('a')
        url = link.get('href', None)
        
        direct_link = {
            "url" : url,
            "visited" : False
        }
        all_links.append(direct_link)

    next_btn = bs.find('a', {'class': 'next'})
    if next_btn:
        current_url = next_btn.get('href')
    else:
        current_url = None


product_dict = []
for link in all_links:
    url = link['url']
    print("VISITING: ", url)

    product_response = requests.get(url, timeout=30)
    product_content = BeautifulSoup(product_response.text, 'html.parser')
    name = product_content.find('h3').get_text(strip=True)
    details = product_content.find_all('p', {'class' : 'card-text'})
    year = details[0].get_text(strip=True)
    mileage = details[1].get_text(strip=True)

    product_info = {
        'name': name,
        'year': year,
        'mileage': mileage
    }
    product_dict.append(product_info) 



with open("cars.json", "w", encoding="utf-8") as file:
      json.dump(all_products, file, indent=4, ensure_ascii=False)

with open("links.json", "w", encoding="utf-8") as file:
        json.dump(all_links, file, indent=4, ensure_ascii=False)


with open("products.json", "w", encoding="utf-8") as file:
    json.dump(product_dict, file, indent=4, ensure_ascii=False)
