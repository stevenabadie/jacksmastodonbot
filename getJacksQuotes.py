import requests
from bs4 import BeautifulSoup as bs

#Fight Club quote source
url = "https://www.rottentomatoes.com/m/fight_club/quotes/"

#Download page for parsing
page = requests.get(url)
parsedPage = bs(page.text, 'html.parser')

print(parsedPage)
