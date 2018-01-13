import requests
from bs4 import BeautifulSoup as bs

# Quote source page from rotten tomatoes
url = "https://www.rottentomatoes.com/m/fight_club/quotes/"

# Request page for parsing
page = requests.get(url)
parsedPage = bs(page.text, 'html.parser')

'''
Early testing of the BeautifulSoup package, will remove later

#print(parsedPage)
#quoteActor = parsedPage.find('span', class_="quote_actor")
#print(quoteActor.next_element.next_element.next_element.next_element)
'''

for quote in parsedPage.find_all('span', class_="quote_actor"):
    line = quote.next_element.next_element.next_element.next_element
    if len(line) <= 500:
        print(len(line))
        print(line + "\n")
