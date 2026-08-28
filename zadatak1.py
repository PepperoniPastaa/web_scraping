import requests
from bs4 import BeautifulSoup

BASE_URL = "https://scrapeme.live/shop/"
response = requests.get (BASE_URL, timeout= 29)

page_content = BeautifulSoup (response.text, "html.parser")
najprvi_h1 = page_content.find ("h1")

print (najprvi_h1)


