from bs4 import BeautifulSoup
from sqlmodel import Session, select, Column, Field, create_engine, SQLModel
from curl_cffi import requests
import json

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    isbn: str
    price: float = Field(default=0.0, ge=0.0)
engine = create_engine("sqlite:///books.db")
SQLModel.metadata.create_all(engine)

url = "https://www.knjizare-vulkan.rs/files/sitemap/SRB_rs/product.xml"

def scrape(url):
    response = requests.get(url, impersonate='chrome120', timeout=30)
    page_cont = BeautifulSoup(response.text, 'html.parser')
    links = page_cont.find_all('loc')
    book_links = [link.text for link in links]
    return book_links

book_links = scrape(url) 

def scrape_book(url):
    response = requests.get(url, impersonate='chrome120', timeout=30)
    page_cont = BeautifulSoup(response.text, 'html.parser')

    book_cont = page_cont.find_all('script', {'type': 'application/ld+json'})

    for element in book_cont:
        try:
            data = json.loads(element.string)
        except (json.JSONDecodeError, TypeError):
            continue
        if data.get('@type') == 'Product' and data.get('isbn'):
            book_dict = {
                "name": data.get('name'),
                "isbn": data.get('isbn'),
                "price": data.get('offers', {}).get('price'),
                }
            return book_dict
    return None

with Session(engine) as session:
    for book_link in book_links:
        book_dict = scrape_book(book_link)

        if book_dict and book_dict["isbn"]:
            print("Scraping:", book_dict["name"])
        
            book = Book(
                name=book_dict["name"],
                isbn=book_dict["isbn"],
                price=float(book_dict["price"])
            )

          
            session.add(book)
            session.commit()



   


