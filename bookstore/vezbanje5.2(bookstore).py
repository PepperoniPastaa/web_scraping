from bs4 import BeautifulSoup
from sqlmodel import Session, select, Column, Field, create_engine, SQLModel
from curl_cffi import requests
import json

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    isbn: str | None = Field(default=None, index=True)
    price: float = Field(default=0.0, ge=0.0)
    brand : str | None= Field(default=None)
    description: str = Field(default=None)
    product_id: str = Field(default=None)
    availability: str = Field(default=None)
    product_url: str = Field(default=None)

engine = create_engine("sqlite:///books.db")
SQLModel.metadata.create_all(engine)

url = "https://www.knjizare-vulkan.rs/files/sitemap/SRB_rs/product.xml"

def scrape(url):
    response = requests.get(url, impersonate='chrome120', timeout=30)
    page_cont = BeautifulSoup(response.text, 'html.parser')
    links = page_cont.find_all('loc')
    product_links = [link.text for link in links]
    return product_links

product_links = scrape(url) 


def scrape_product(url):
    response = requests.get(url, impersonate='chrome120', timeout=30)
    page_cont = BeautifulSoup(response.text, 'html.parser')

    product_cont = page_cont.find_all('script', {'type': 'application/ld+json'})

    for element in product_cont:
        try:
            data = json.loads(element.string)
        except (json.JSONDecodeError, TypeError):
            continue
        if data.get('@type') == 'Product':
            book_dict = {
                "name": data.get('name'),
                "isbn": data.get('isbn'),
                "price": data.get('offers', {}).get('price'),
                "brand": data.get('brand', {}).get('name'),
                "description": data.get('description'),
                "product_id": data.get('productID'),
                "availability": data.get('offers', {}).get('availability'),
                "product_url": url
                }
            return book_dict
    return None

with Session(engine) as session:
    for product_link in product_links:
        product_dict = scrape_product(product_link)

        print("Checking productID...", product_dict["name"], "| ID:", product_dict["product_id"])
        
        if product_dict:
            existing_product = session.exec(select(Product).where(Product.product_id == product_dict["product_id"])).first()

        if not product_dict["product_id"]:
            print(f"Already in the database.", product_dict["name"])
            break
        else:

            print("Scraping...", product_dict["name"])
            
            product = Product(
            name=product_dict["name"],
            isbn=product_dict["isbn"],
            price=float(product_dict["price"]),
            brand=product_dict["brand"],
            description=product_dict["description"],
            product_id=product_dict["product_id"],
            availability=product_dict["availability"],
            product_url=product_dict["product_url"]    
        )

            
        session.add(product)
        session.commit()



   


