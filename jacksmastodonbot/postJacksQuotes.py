import inspect
import json
import os
from mastodon import Mastodon


class PostJacksQuotes:
    def __init__(self):
        self.scriptLocation = os.path.dirname(inspect.getfile(self.__class__))

        with open(self.scriptLocation + '/botConfig.json', 'r') as botConfigFile:
            botConfig = json.load(botConfigFile)

        # Create Mastodon API instance
        self.mastodon = Mastodon(
            client_id=self.scriptLocation + '/' + botConfig.get('botName') + '_clientcred.secret',
            access_token=self.scriptLocation + '/' + botConfig.get('botName') + '_usercred.secret',
            api_base_url=botConfig.get('mastodonServerUrl'),
            request_timeout=20
        )

        # Create nextQuote and try to load nextQuote.json into it. If nextQuote.json
        # does not exist, create the file and assign 0 to nextQuote. nextQuote is used
        # to track which quote in the list is next to post.
        self.nextQuote = None
        try:
            with open(self.scriptLocation + '/nextQuote.json', 'r') as nextQuoteFile:
                self.nextQuote = int(json.load(nextQuoteFile))
        except Exception:
            with open(self.scriptLocation + '/nextQuote.json', 'w') as nextQuoteFile:
                json.dump(self.nextQuote, nextQuoteFile)
            self.nextQuote = 0

        # Load quotes.json into quoteList
        with open(self.scriptLocation + '/quotes.json', 'r') as quoteFile:
            self.quoteList = json.load(quoteFile)


    def postQuote(self):
        # Post quote if there are unposted quotes. Otherwise, raise an exception.
        if self.nextQuote <= len(self.quoteList):
            self.mastodon.toot(self.quoteList[self.nextQuote])
        else:
            raise StopIteration("There are no quotes left to post")

        # Increase nextQuote by one and dump to nextQuote.json. The next time the
        # script is run the next quote in the list will be used.
        self.nextQuote += 1
        with open(self.scriptLocation + '/nextQuote.json', 'w') as nextQuoteFile:
            json.dump(self.nextQuote, nextQuoteFile)
