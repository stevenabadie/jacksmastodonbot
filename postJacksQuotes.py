import json
from mastodon import Mastodon
from createJacksApp import botName, mastodonServerUrl

# Create Mastodon API instance
mastodon = Mastodon(
    client_id = botName + '_clientcred.secret',
    access_token = botName + '_usercred.secret',
    api_base_url = mastodonServerUrl,
    request_timeout = 20
)

# Create nextQuote and try to load nextQuote.json into it. If nextQuote.json
# does not exist, create the file and assign 0 to nextQuote. nextQuote is used
# to track which quote in the list is next to post.
nextQuote = None
try:
    with open('nextQuote.json', 'r') as nextQuoteFile:
        nextQuote = int(json.load(nextQuoteFile))
except Exception:
    with open('nextQuote.json', 'w') as nextQuoteFile:
        json.dump(nextQuote, nextQuoteFile)
    nextQuote = 0

# Load quotes.json into quoteList
with open('quotes.json', 'r') as quoteFile:
    quoteList = json.load(quoteFile)

# Post quote if there are unposted quotes. Otherwise, raise an exception.
if nextQuote <= len(quoteList):
    mastodon.toot(quoteList[nextQuote])
else:
    raise StopIteration("There are no quotes left to post")

# Increase nextQuote by one and dump to nextQuote.json. The next time the
# script is run the next quote in the list will be used.
nextQuote += 1
with open('nextQuote.json', 'w') as nextQuoteFile:
    json.dump(nextQuote, nextQuoteFile)
