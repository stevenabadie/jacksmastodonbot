import requests
import json
from Levenshtein import ratio
from bs4 import BeautifulSoup as bs

compareRatio = 0.75

# Quote source page from rotten tomatoes
url = "https://www.rottentomatoes.com/m/fight_club/quotes/"

# Request page from url, parse for use with bs, and set to parsedPage
page = requests.get(url)
parsedPage = bs(page.text, 'html.parser')

# Create quoteList and load quotes.json into it.
# quotes.json is created if it does not already exist
quoteList = []
try:
    with open('quotes.json', 'r') as quoteFile:
        quoteList = json.load(quoteFile)
except Exception:
    with open('quotes.json', 'w') as quoteFile:
        json.dump(quoteList, quoteFile)

# Find all quotes in parsedPage and append to quoteList
for quote in parsedPage.find_all('span', class_="quote_actor"):
    line = quote.next_element.next_element.next_element.next_element
    if len(line) <= 500 and len(line) > 5:
        if all(ratio(line, x) < compareRatio for x in quoteList):
            quoteList.append(line)
        else:
            pass

with open('quotes.json', 'w') as quoteFile:
    json.dump(quoteList, quoteFile)

# This is only here for testing and will be removed later
for quote in quoteList:
    print(str(quote) + "\n")
