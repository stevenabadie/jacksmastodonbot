import json
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

botConfig = {}
try:
    with open('botConfig.json', 'r') as botConfigFile:
        botConfig = json.load(botConfigFile)
except Exception:
    botName = input('Enter a name for your Mastodon bot: ')
    mastodonServerUrl = input('Enter the Mastodon server url (https://botsin.space): ')
    userEmail = input('Enter the email associated with your Mastodon account: ')
    userPass = input('Enter the pass word for you Mastodon account: ')

    botConfig.update(
        botName= botName,
        mastodonServerUrl= mastodonServerUrl,
        userEmail= userEmail,
        userPass= userPass
    )
    with open('botConfig.json', 'w') as botConfigFile:
        json.dump(botConfig, botConfigFile)

# Geerate the client id and client secret tokens and saves them to a file
Mastodon.create_app(
     botConfig.get('botName'),
     api_base_url = botConfig.get('mastodonServerUrl'),
     scopes=['write'], # This bot only writes
     to_file = botConfig.get('botName') + '_clientcred.secret'
)

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
