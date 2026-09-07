import requests
import json
from bs4 import BeautifulSoup
import uuid

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
counter = 1
for link in all_links:
    try:
        url = link['url']
        print("VISITING: ", url)
        if link['visited'] == False:

            product_response = requests.get(url, timeout=30)
            print("Working on product ", counter)
            counter +=1
            product_content = BeautifulSoup(product_response.text, 'html.parser')

            name = product_content.find('h2', {'class': 'title'}).get_text(strip=True)
            price = product_content.find('h3', {'class': 'price'}).get_text(strip=True)
            year = product_content.find('td', {'class': 'year'}).get_text(strip=True)
            mileage = product_content.find('td', {'class': 'mileage'}).get_text(strip=True)

            product_info = {
                'id' : str(uuid.uuid4()),
                'name': name,
                'price': price,
                'year': year,
                'mileage': mileage
            }
            product_dict.append(product_info)
            link ['visited'] = True
            with open("products.json", "w", encoding="utf-8") as file:
                json.dump(product_dict, file, indent=4, ensure_ascii=False)

    except Exception as e:
         print(e) 



with open("cars.json", "w", encoding="utf-8") as file:
      json.dump(all_products, file, indent=4, ensure_ascii=False)

with open("links.json", "w", encoding="utf-8") as file:
        json.dump(all_links, file, indent=4, ensure_ascii=False)



