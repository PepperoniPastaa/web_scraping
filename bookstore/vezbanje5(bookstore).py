from bs4 import BeautifulSoup
from curl_cffi import requests
import json
from sqlmodel import JSON, Column, Session, select, Field, SQLModel, create_engine

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    isbn: str
    price: float = Field(default=0.0, ge=0.0)

engine = create_engine("sqlite:///books.db")
SQLModel.metadata.create_all(engine)

url = "https://www.knjizare-vulkan.rs/roman/312774-alisa-u-zemlji-ideja"

def scrape_book(url):
    response = requests.get(url, impersonate='chrome120', timeout=30)
    page_cont = BeautifulSoup(response.text, 'html.parser')

    book_cont = page_cont.find_all('script', {'type': 'application/ld+json'})

    for element in book_cont:
        data = json.loads(element.string)

        if data.get('@type') == 'Product':
            book_dict = {
                "name": data.get('name'),
                "isbn": data.get('isbn'),
                "price": data.get('offers', {}).get('price'),
                }
            return book_dict
    return None
book_dict = scrape_book(url)
print(book_dict)

with Session(engine) as session:
    book = Book(
        name=book_dict["name"],
        isbn=book_dict["isbn"],
        price=float(book_dict["price"])
    )

    session.add(book)
    session.commit()

    print(book)


