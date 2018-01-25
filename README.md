# I am Jack's Mastodon bot.

This is a simple Mastodon bot that posts movie quotes from IMDb quote pages.

Jack's Mastodon bot uses a few great Free and Open Soure Python packages.
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](http://docs.python-requests.org/en/master/)
* [Mastodon.py](https://github.com/halcy/Mastodon.py)

## Setup
1. Clone the repo and change into the project directory

    `git clone https://gitea.anothernewthing.com/steven/jacks-mastodon-bot.git`  
    `cd jacks-mastodon-bot`

2. Install required packages. You can use the includes PyPI requirements.txt  or other package managers to install all of the required packages. You will need Python 3.  

    ### PyPI  
    `pip install requirements.txt`
    
    ### Fedora  
    `dnf install python3-Mastodon python3-beautifulsoup4`

    Otherwise, you need the following requirements:
    * Python 3
    * Mastodon.py
    * Beautiful Soup 4
    * Requests

3. Create an account on a Mastodon server.

4. Run jacksBotSetup.py. This will ask you to enter a number of items:
    * The URL for an IMDb quotes page. This bot was built from the [Fight Club](http://www.imdb.com/title/tt0137523/quotes) quotes page for example
    * A name for you bot.
    * The URL for the Mastodon server you created your account on. http://botsin.space is a server for testing and running Mastodon bots.
    * The email you used for the Mastodon account you created.
    * The password for the Mastodon account you created.

5. Run postJacksQuotes.py. Everytime this script is run a new quote will be posted to your Mastodon account. You can schedule the script using cron or another scheduler.
