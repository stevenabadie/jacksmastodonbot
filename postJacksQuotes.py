from mastodon import Mastodon
from createJacksApp import botName, mastodonServerUrl

# Create API instance
mastodon = Mastodon(
    client_id = botName + '_clientcred.secret',
    access_token = botName + '_usercred.secret',
    api_base_url = mastodonServerUrl
)

mastodon.toot('This is a test tootoot.')
