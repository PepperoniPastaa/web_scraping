import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://scrapeme.live/shop/"


all_articles_links = []
current_url = BASE_URL

while current_url:

    response = requests.get(current_url, timeout=29)

    page_content = BeautifulSoup(response.text, "html.parser")
    all_cards = page_content.find_all("li", {"class": "type-product"})

    print ("Acquiring links...")


    for card in all_cards:
        link = card.find("a")
        url = link.get("href", None)

        dict_links = {
        "url" : url,
        "visited" : False
        }

        if url is not None:
            all_articles_links.append(dict_links)
            if len(all_articles_links) % 40 == 0:
                print (f"{len(all_articles_links)} links have been scraped :)")
        else:
                print("Url not found, wompica.")

    with open ("links.json", "w", encoding="utf-8") as file:
        json.dump(all_articles_links, file, indent=4, ensure_ascii= False)

    next_btn = page_content.find("a", {"class": "next"})
    if next_btn:
         current_url = next_btn.get("href")
    else:
         current_url = None


pokemons = []
for link in all_articles_links:
    if link["visited"] == False:
        response = requests.get(link["url"], timeout=28)

        articles_content = BeautifulSoup (response.text, "html.parser")

        name = articles_content.find ("h1", {"class": "product_title"})
        name = name.get_text(strip=True)

        price = articles_content.find ("span", {"class": "price"})
        price = price.get_text(strip=True)


        tags_container = articles_content.find("span", {"class": "tagged_as"})
        if tags_container:
            tags = [
                tag.get_text(strip=True)
                for tag in tags_container.find_all("a")  
            ]
        else:
            tags = []


        categories_container = articles_content.find_all("span", {"class": "posted_in"})
        if categories_container:
            categories = [
            category.get_text(strip=True)
                for category in categories_container.find("a")
            ]
        else:
            categories = []


        pokemon_dict = {
            "name" : name,
            "price" : price,
            "tags" : tags, 
            "category" : categories
        }

        pokemons.append(pokemon_dict)

        link ["visited"] = True




with open("pokemon_data.json", "w", encoding="utf-8") as file:
    json.dump(pokemons, file, indent=4, ensure_ascii= False)


    print(pokemon_dict)
   
     






