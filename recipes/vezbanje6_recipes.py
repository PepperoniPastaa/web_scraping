from bs4 import BeautifulSoup
from curl_cffi import requests
import json

url = 'https://www.allrecipes.com/'

def scrape_recipe(url):
    response = requests.get(url, impersonate='chrome120', timeout=30)

    page_content = BeautifulSoup(response.text, 'html.parser')

    recipe_cont = page_content.find('script', {'type': 'application/ld+json'})
    recipe_dict = json.loads(recipe_cont.string)

    return recipe_dict

recipe_dict = scrape_recipe(url)
print(recipe_dict)

