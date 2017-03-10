## GIGTAT twitter alerts

This script will check music festival twitter accounts and will scan tweets looking for keywords. If keywords are found an email is sent with the twitter account and tweet text. See gigtat_twitter_alert.py for accounts and kewords.

### USE 

1) Create a Twitter user account if you don't have one already.
Go to https://apps.twitter.com/ and log in with your Twitter user account. 

2) Get dev account under same name and get your twitter keys:

* Click “Create New App”
* Fill out the form, agree to the terms, and click “Create your Twitter application”
* In the next page, click on “Keys and Access Tokens” tab, and copy your “API key” and “API secret”. Scroll down and click “Create my access token”, and copy your “Access token” and “Access token secret”. 

3) Add your keys to settings.py

4) Add email credentials and recipient to settings.py (you may need to enable access for less secure apps for your email account)

5) Make sure you are running Python 3.X and install libraries in requirements.txt (pip install -r /path/to/requirements.txt)

6) Run script (python gigtat_twitter_alert.py) or add it to cron to run every X min.