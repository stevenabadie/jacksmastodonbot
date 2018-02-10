# I am Jack's Mastodon Bot.

A simple Mastodon bot that grabs movie quotes from IMDb quote pages and posts them to Mastodon. It is currently only setup for and tested on GNU/Linux.

Jack's Mastodon bot uses a few great Free and Open Soure Python packages.
* [Requests](http://docs.python-requests.org/en/master/) -- Used to grab HTML data from IMDb quote pages.
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) -- Used to parse the raw HTML and prepare quotes for posting.
* [Mastodon.py](https://github.com/halcy/Mastodon.py) -- Used to register app with Mastodon and post quotes.

## Setup
1. Create an account on a Mastodon server. https://botsin.space is a good server for testing and running bots.  

2. Find a quotes page for a movie or show on [IMDb.com](http://www.imdb.com). You can generally find the quotes page listed in the _Did You Know?_ section on movie or show pages. The example page used to develop this bot was the quotes page for [Fight Club](http://www.imdb.com/title/tt0137523/quotes).

    **Tip**: Mastodon posts have a max of 500 characters so look for movies or shows with a majority of short quote entries. Otherwise, you may get a small number of postable quotes.

3. Clone the repo and change into the project directory

    `git clone https://gitlab.com/stevenabadie/jacksmastodonbot.git`  
    `cd jacksmastodonbot`

4. Create a virtual environment and activate it. Here the environment is named *botenv* but you can name it whatever you want.

    `python3 -m venv botenv`  
    `source botenv/bin/activate`  

5. Install jacksmastodonbot and required packages. This step requires `pip` which should already be installed if you have Python 3.4 or greater. If not, follow [these instructions](https://pip.pypa.io/en/stable/installing/).  

    `pip install .`        

6. Setup your bot configuration.

    `setup-jacks-bot`

    After running `setup-jacks-bot` you will be prompted with requests for information to configure your bot.
      * The URL for an IMDb quotes page.
      * A name for you bot.
      * The URL for the Mastodon server you created your account on.
      * The email you used for the Mastodon account you created.
      * The password for the Mastodon account you created.  

5. Your bot is now ready to post quotes. To post a quote run:

    `post-quote`

    You can use cron or anoher scheduler to schedule post-quote. [Here is a quick guide on setting up a cron job](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-on-a-vps). An example cron setting for posting a new quote every hour would be:

    `0 * * * * /home/YOURUSER/jacksmastodonbot/botenv/bin/post-quote`

    **Tip**: beware how often you are posting with your bot. If the frequency is too quick it could be considered spam depending on the rules of the Mastodon server you are posting to.
