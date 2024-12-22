import requests
from bs4 import BeautifulSoup

req = requests.get("https://www.geekforgeeks.org/")

soup = BeautifulSoup(req.content, "html.parser")

res = soup.href

print(res.prettify())