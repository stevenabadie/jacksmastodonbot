import requests
import json
from bs4 import BeautifulSoup as bs

# Quote source page from rotten tomatoes
url = "http://www.imdb.com/title/tt0137523/quotes"

# Request page from url, parse for use with bs, and set to parsedPage
page = requests.get(url)
parsedPage = bs(page.text, 'html.parser')

# Create quoteList and try to load quotes.json into it.
# quotes.json is created if it does not already exist
quoteList = []
try:
    with open('quotes.json', 'r') as quoteFile:
        quoteList = json.load(quoteFile)
except Exception:
    with open('quotes.json', 'w') as quoteFile:
        json.dump(quoteList, quoteFile)

# Find all quotes in parsedPage and append to quoteList
for entry in parsedPage.find_all('div', class_="sodatext"):
    # Find the quote character name and assign to character variable. Quotes
    # that have multiple characters and lines are skipped.
    if len(entry.find_all('span', class_="character")) > 1:
        continue
    else:
        character = entry.find('span', class_="character").next_element
    # Find the quote line and assign to line variable. Quotes on IMDb.com have
    # a number of differing formats that require detection and then correction
    # for extra characters and/or line breaks.
    #
    # For quotes with time stamps like, [1:04:02], the closing square bracket
    # and line break have to be removed.
    if "]" in str(entry):
        lineBad = character.next_element.next_element.next_element.next_element
        line = str(lineBad).replace("]\n", ": ")
    # Some quotes contain a line break. Detect if there is a line break in a
    # quote line and remove if found.
    elif "\n" in character.next_element.string:
        lineBad = character.next_element.string
        line = str(lineBad).replace("\n", " ")
    else:
        line = str(character.previous_element)
    # Join the character and line and assign to quote variable
    quote = str(character) + str(line)
    # Mastodon toot posts are limited to 500 characters or less. Check if quote
    # length is 500 characters or less and append to quoteList if so. Quotes
    # larger than 500 characters will be passed and not added to quoteList.
    if len(quote) <= 500 and len(line) > 5:
        quoteList.append(quote)
    else:
        pass

# Dump quoteFile list into quotes.json file
with open('quotes.json', 'w') as quoteFile:
    json.dump(quoteList, quoteFile)


# Can be used for testing to print quote lines to terminal output
for quote in quoteList[0:]:
    print(str(quote) + "\n")


# Leftover code from Rottentomatoes parsing that attempted to deal with
# with duplicates. IMDb does not appear to have the same issue but leaving
# for now.
'''
from Levenshtein import ratio
#compareRatio = 0.75
for quote in parsedPage.find_all('div', class_="sodatext"):
    line = quote.next_element.next_element.next_element.next_element
    if len(line) <= 500 and len(line) > 5:
        if all(ratio(line, x) < compareRatio for x in quoteList):
            quoteList.append(line)
        else:
            pass
            with open('quotes.json', 'w') as quoteFile:
                json.dump(quoteList, quoteFile)
'''
