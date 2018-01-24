import json
import requests
from bs4 import BeautifulSoup as bs
from mastodon import Mastodon

# To connect your bot through the Mastodon API you need to first create an
# account on the Mastodon server of your choice. https://botsin.space is a
# great Mastodon server for testing bots.
#
# Once you have your account created, run this script. You will be prompted to
# enter your bot name, the Mastodon server url, the email you used with your
# Mastodon account, and your Mastadon account password. This information will
# then be stored in botConfig.json
#
# The script then generates the client id, client secret, and client access
# tokens. This will generate two files to store the tokens.

def createJacksApp():
    botConfig = {}
    try:
        with open('botConfig.json', 'r') as botConfigFile:
            botConfig = json.load(botConfigFile)
    except Exception:
        quoteUrl = input('Enter the URL for the IMDb quote page you want to use to generate quote posts from: ')
        botName = input('Enter a name for your Mastodon bot: ')
        mastodonServerUrl = input('Enter the Mastodon server url (https://botsin.space): ')
        userEmail = input('Enter the email associated with your Mastodon account: ')
        userPass = input('Enter the pass word for you Mastodon account: ')

        botConfig.update(
            quoteUrl = quoteUrl,
            botName= botName,
            mastodonServerUrl= mastodonServerUrl,
            userEmail= userEmail,
            userPass= userPass
        )
        with open('botConfig.json', 'w') as botConfigFile:
            json.dump(botConfig, botConfigFile)
        print('Your bot info is now saved in botConfig.json. Time to create the Mastodon app')

    # Geerate the client id and client secret tokens and saves them to a file
    Mastodon.create_app(
         botConfig.get('botName'),
         api_base_url = botConfig.get('mastodonServerUrl'),
         scopes=['write'], # This bot only writes
         to_file = botConfig.get('botName') + '_clientcred.secret'
    )
    print('Client ID and Client secret received and saved to file')

    # Connect the app to your account and save generated access token to a file
    mastodon = Mastodon(
        client_id = botConfig.get('botName') + '_clientcred.secret',
        api_base_url = botConfig.get('mastodonServerUrl')
    )
    mastodon.log_in(
        botConfig.get('userEmail'),
        botConfig.get('userPass'),
        scopes=['write'], # This bot only writes
        to_file = botConfig.get('botName') + '_usercred.secret'
    )
    print('App connected to your account and access token received and saved to file.')


def getJacksQuotes():
    try:
        with open('botConfig.json', 'r') as botConfigFile:
            botConfig = json.load(botConfigFile)
    except Exception:
        raise NameError('You are missing the botConfig.json file')

    # Request page from url, parse for use with bs, and set to parsedPage
    page = requests.get(botConfig.get('quoteUrl'))
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
    print('Page source pulled from url and ready for parsing.')

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

    print('Quotes filtered, saved to quotes.json and ready for posting! \n',
          'Now run postJacksQuotes.py or set up a cron for scheduled toots.')

createJacksApp()
getJacksQuotes()
