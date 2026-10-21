from sqlmodel import Session, select, Column, Field, create_engine, SQLModel
from curl_cffi import requests
from html.parser import HTMLParser
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup




url = "https://www.knjizare-vulkan.rs/contemporary-fiction/316277-dead-poets-society"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    html = page.content()
    browser.close()

    soup = BeautifulSoup(html, 'html.parser')

    name = soup.select_one('h1.nb-title').get_text(strip = True)
    price = soup.select_one('span', {'class': 'nb-price-value'}).get_text(strip = True)
    description = soup.select_one('div.nb-product-short-description').get_text(strip = True)


    print("Name:", name)
    print("Price:", price)
    print("Description:", description)
    

  

   


