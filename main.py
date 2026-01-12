import requests
from bs4 import BeautifulSoup

url1 = "https://www.business-senegal.com/fre/Entreprises/profilsample/1/annonceur"
url2 = "/fre/Entreprises/profilsample/1/annonceur"

# url = url_base + url2

response = requests.get(url2)
soup = BeautifulSoup(response.content, 'html.parser')

print(soup)

