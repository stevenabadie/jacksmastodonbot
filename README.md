# I am Jack's Mastodon bot.

This is a simple Mastodon bot that posts movie quotes from IMDb quote pages.

Jack's Mastodon bot uses a few great Free and Open Soure Python packages.
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](http://docs.python-requests.org/en/master/)
* [Mastodon.py](https://github.com/halcy/Mastodon.py)

## Basic Setup
1. Clone the repo and change into the project directory
```
git clone https://gitea.anothernewthing.com/steven/jacks-mastodon-bot.git
cd jacks-mastodon-bot
```
2. Install required packages
`pip install requirements.txt`
3. Edit getJacksQuotes.py and change the url field to the IMDb quote page you want to pull quotes from. This bot was built from the [Fight Club](http://www.imdb.com/title/tt0137523/quotes) quotes page.
4. Run getJacksQuotes.py. It should create a quotes.json file full of quotes separated by a blank line.
5. Make an account on a Mastodon server. [http://botsin.space](http://botsin.space) is a good server for testing and running Mastodon bots.
6. Run createJacksApp.py. You will be prompted to fill in your bot name, the Mastodon server you create your account on, the email you used to create your Mastodon account, and your Mastodon account password. Once the script is complete you should now see three new files: yourbotname_clientcred.secret, yourbotname_usercred.secret, and botConfig.json.
7. Run postJacksQuotes.py. Everytime this script is run a new quote will be posted to your Mastodon account.
