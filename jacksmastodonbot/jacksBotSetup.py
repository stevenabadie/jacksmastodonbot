import inspect
import json
import os
import requests
from bs4 import BeautifulSoup as bs
from mastodon import Mastodon

# To connect your bot through the Mastodon API you need to first create an
# account on the Mastodon server of your choice. https://botsin.space is a
# great Mastodon server for testing bots.


class JacksBotSetup:
    """Setup the Mastodon bot

    The setup will request information to generate keys for access to your Mastodon account, scrape a chosen IMDb movie quote page and parse the quotes for posting.
    """

    def __init__(self):
        self.scriptLocation = os.path.dirname(inspect.getfile(self.__class__))

    def createJacksApp(self):
        """Request bot information and generate botConfig.json and access tokens

        Request bot setup information including IMDb quote page url, bot name, Mastodon server for your account, Mastodon account email, and Mastodon account password. This info is stored in botConfig.json. The botConfig information is then used to register the bot with the given Mastodon account and generate access tokens.
        """
        botConfig = {}
        try:
            with open(self.scriptLocation + '/botConfig.json', 'r') as botConfigFile:
                botConfig = json.load(botConfigFile)
        except Exception:
            quoteUrl = input('Enter the URL for the IMDb quote page you want to use to generate quote posts from: ')
            botName = input('Enter a name for your Mastodon bot: ')
            mastodonServerUrl = input('Enter the Mastodon server url (https://botsin.space): ')
            userEmail = input('Enter the email associated with your Mastodon account: ')
            userPass = input('Enter the pass word for you Mastodon account: ')

            botConfig.update(
                quoteUrl=quoteUrl,
                botName=botName,
                mastodonServerUrl=mastodonServerUrl,
                userEmail=userEmail,
                userPass=userPass
            )
            with open(self.scriptLocation + '/botConfig.json', 'w') as botConfigFile:
                json.dump(botConfig, botConfigFile)
            os.chmod(self.scriptLocation + '/botConfig.json', 0o660)
            print('Your bot info is now saved in botConfig.json. Time to create the Mastodon app')

        # Generate the client id and client secret tokens and saves them to a file
        Mastodon.create_app(
             botConfig.get('botName'),
             api_base_url=botConfig.get('mastodonServerUrl'),
             scopes=['write'],  # This bot only writes
             to_file=self.scriptLocation + '/' + botConfig.get('botName') + '_clientcred.secret'
        )
        os.chmod(self.scriptLocation + '/' + botConfig.get('botName') + '_clientcred.secret', 0o660)
        print('Client ID and Client secret received and saved to file')

        # Connect the app to your account and save generated access token to a file
        mastodon = Mastodon(
            client_id=self.scriptLocation + '/' + botConfig.get('botName') + '_clientcred.secret',
            api_base_url=botConfig.get('mastodonServerUrl')
        )
        mastodon.log_in(
            botConfig.get('userEmail'),
            botConfig.get('userPass'),
            scopes=['write'],  # This bot only writes
            to_file=self.scriptLocation + '/' + botConfig.get('botName') + '_usercred.secret'
        )
        os.chmod(self.scriptLocation + '/' + botConfig.get('botName') + '_usercred.secret', 0o660)
        print('App connected to your account and access token received and saved to file.')

    def lineCorrection(self, quoteEntry, character):
        """Find the quote line, correct detected formatting issues, and assign to line variable.

        Quotes on IMDb.com have a number of differing formats that require detection and then correction for extra characters and/or line breaks.
        For quotes with time stamps like, [1:04:02], the closing square bracket and line break have to be removed.
        """

        if "]" in str(character.next_element.next_element.next_element.next_element):
            lineBad = \
                (character.next_element.next_element.next_element.next_element)
            line = str(lineBad).replace("]\n", ": ")
        # Sometimes there will be a random bullet point in a quote.
        elif "<li>" in str(character.next_element.next_element.next_element):
            line = ": " + str(character.next_element.next_element.next_element.string)
        # Some quotes contain a line break. Detect if there is a line break in
        # a quote line and remove if found.
        elif "\n" in character.next_element.string:
            lineBad = character.next_element.string
            line = str(lineBad).replace("\n", " ")
        else:
            line = str(character.previous_element)
        return(line)

    def getJacksQuotes(self):
        """Scrape quote data from given IMDb quote url and parse for posting.

        Using requests, the HTML is scraped from the IMDb quote url in botConfig and assigned to page. beautifulsoup4 is then used to parse the html to recognize postable quotes and append quotes to quoteList. Once processing is complete quoteList is saved to quotes.json.
        """
        try:
            with open(self.scriptLocation + '/botConfig.json', 'r') as botConfigFile:
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
            with open(self.scriptLocation + '/quotes.json', 'r') as quoteFile:
                quoteList = json.load(quoteFile)
        except Exception:
            with open(self.scriptLocation + '/quotes.json', 'w') as quoteFile:
                json.dump(quoteList, quoteFile)
        print('Page source pulled from url and ready for parsing.')

        # Find all quotes in parsedPage and append to quoteList
        for entry in parsedPage.find_all('div', class_="sodatext"):
            # Check if there are more than one character line in a quote. If so,
            # iterate over the quote lines and append to quote variable.
            if len(entry.find_all('span', class_="character")) > 1:
                quote = ""
                for characterLine in entry.find_all('span', class_="character"):
                    character = characterLine.next_element
                    line = self.lineCorrection(characterLine, character)
                    quoteLine = str(character) + str(line)
                    quote += str(quoteLine) + "\n"
                quote = quote[0:quote.rfind("\n")]
            else:
                # Find the quote character name and assign to character variable.
                # Quotes that have multiple characters and lines are skipped.
                character = entry.find('span', class_="character").next_element
                line = self.lineCorrection(entry, character)
                quote = str(character) + str(line)
            # Mastodon toot posts are limited to 500 characters or less. Check if
            # quote length is 500 characters or less and append to quoteList if so.
            # Quotes larger than 500 characters will be passed and not added to
            # quoteList.
            if len(quote) <= 500 and len(line) > 5:
                quoteList.append(quote)
            else:
                pass

        # Dump quoteFile list into quotes.json file
        with open(self.scriptLocation + '/quotes.json', 'w') as quoteFile:
            json.dump(quoteList, quoteFile)

        print('Quotes filtered, saved to quotes.json and ready for posting!')
