from bs4 import BeautifulSoup
from curl_cffi import requests
import json
from sqlmodel import Session, select, Column, Field, create_engine, SQLModel
from html.parser import HTMLParser


class Recipe(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str | None = None
    author: str | None = None
    description: str | None = None
    category: str | None = None
    cuisine: str | None = None
    ingredients: str | None = None
    calories: str | None = None
    protein: str | None = None
    fat: str | None = None
    rating: str | None = None

engine = create_engine("sqlite:///recipes.db")
SQLModel.metadata.create_all(engine)


url = 'https://www.allrecipes.com/sitemap_1.xml'
http = requests.Session()

def scrape(url):
    response = http.get(url, impersonate = 'chrome120', timeout=30)
    content = BeautifulSoup(response.text, 'xml')

    links = []

    for element in content.find_all('loc'):
        links.append(element.text)
    return links

product_links = scrape(url)
print ("Links found: ", len(product_links))
    



def scrape_recipe(url):
    response = http.get(url, impersonate = 'chrome120', timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')

    json_ld = soup.find_all('script', type='application/ld+json')

    for element in json_ld:
        try:
            data = json.loads(element.string)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and 'Recipe' in item.get('@type', []):
                    data = item
                    break
            else:
                continue

        if isinstance(data, dict) and 'Recipe' in data.get('@type', []):
            author = data.get('author', [])
            nutrition = data.get('nutrition', {})
            rating = data.get('aggregateRating', {})

            recipe_dict = {
                "name": data.get('name'),
                "author": author[0].get('name') if author else None,
                "description": data.get('description'),
                "category": data.get('recipeCategory'),
                "cuisine": data.get('recipeCuisine'),
                "ingredients": data.get('recipeIngredient'),
                "calories": nutrition.get('calories'),
                "protein": nutrition.get('proteinContent'),
                "fat": nutrition.get('fatContent'),
                "rating": rating.get('ratingValue')

            }
            return recipe_dict
    return None

recipes = []

with Session(engine) as session:
    for index, link in enumerate(product_links, start=1):
        recipe_dict = scrape_recipe(link)
        if recipe_dict is not None:
            recipe_dict["category"] = json.dumps(recipe_dict["category"])
            recipe_dict["cuisine"] = json.dumps(recipe_dict["cuisine"])
            recipe_dict["ingredients"] = json.dumps(recipe_dict["ingredients"])

            recipe = Recipe(**recipe_dict)
            session.add(recipe)
            recipes.append(recipe_dict)
        if len(recipes) % 20 == 0:
            session.commit()

            print("Scraped recipes:", index)
            recipes.clear()



       

