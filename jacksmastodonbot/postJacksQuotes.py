import json
import os
from mastodon import Mastodon

scriptLocation = os.path.dirname(os.path.realpath(__file__))

postJacksQuotes():
    with open(scriptLocation + '/botConfig.json', 'r') as botConfigFile:
            botConfig = json.load(botConfigFile)

    # Create Mastodon API instance
    mastodon = Mastodon(
        client_id=scriptLocation + '/' + botConfig.get('botName') + '_clientcred.secret',
        access_token=scriptLocation + '/' + botConfig.get('botName') + '_usercred.secret',
        api_base_url=botConfig.get('mastodonServerUrl'),
        request_timeout=20
    )

    # Create nextQuote and try to load nextQuote.json into it. If nextQuote.json
    # does not exist, create the file and assign 0 to nextQuote. nextQuote is used
    # to track which quote in the list is next to post.
    nextQuote = None
    try:
        with open(scriptLocation + '/nextQuote.json', 'r') as nextQuoteFile:
            nextQuote = int(json.load(nextQuoteFile))
    except Exception:
        with open(scriptLocation + '/nextQuote.json', 'w') as nextQuoteFile:
            json.dump(nextQuote, nextQuoteFile)
        nextQuote = 0

    # Load quotes.json into quoteList
    with open(scriptLocation + '/quotes.json', 'r') as quoteFile:
        quoteList = json.load(quoteFile)

    # Post quote if there are unposted quotes. Otherwise, raise an exception.
    if nextQuote <= len(quoteList):
        mastodon.toot(quoteList[nextQuote])
    else:
        raise StopIteration("There are no quotes left to post")

    # Increase nextQuote by one and dump to nextQuote.json. The next time the
    # script is run the next quote in the list will be used.
    nextQuote += 1
    with open(scriptLocation + '/nextQuote.json', 'w') as nextQuoteFile:
        json.dump(nextQuote, nextQuoteFile)
