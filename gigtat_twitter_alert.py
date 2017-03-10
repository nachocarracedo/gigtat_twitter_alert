from twython import Twython
import pandas as pd
import settings 
import os.path
import smtplib


if __name__ == "__main__":
	####### Init
	tweet_text_hit= []
	tweet_date_hit= []
	tweet_id_hit = []
	tweet_account_hit = []
	last_tweet_id = []

	# festivals twitter accounts
	festivals = ['@mysteryland', '@MovementDetroit','@nocturnalwland',
				 '@BeyondWland', '@lcpeachfestival','@Bumbershoot' ,
				 '@ElectricZooNY' ,'@JamboOfficial','@buckeye_fest',
				 '@bcsuperfest','@country500','@Boston_Calling',
				 '@TOCFestival','@Hangoutfest','@BealeStMusicFes' ,
				 '@VoodooNola','@acltv' ,'@Newportfolkfest','@CountryMusic' ,
				 '@burningman','@GovBallNYC','@PanoramaNYC','@LiveAtFirefly' ,
				 '@Sasquatch','@lollapalooza','@pitchforkfest',
				 '@Summerfest','@Stagecoach','@sfoutsidelands',
				 '@festivaltortuga','@ultra','@Bonnaroo',
				 '@EDC_LasVegas','@coachella']

	# kewords to look for
	keywords = ['set time','settime','schedule','timetable']   

	####### twython auth
	twitter = Twython(settings.APP_KEY,
					  settings.APP_SECRET,
					  settings.OAUTH_TOKEN,
					  settings.OAUTH_TOKEN_SECRET)

	####### Incremental search since last tweet scanned
	incremental = False
	if os.path.isfile("./csv/last_tweet.csv"):
		last_tweet = pd.read_csv("./csv/last_tweet.csv",encoding='utf-8')
		incremental = True
		
	####### Get and scan tweets 
	for festival_id in festivals:
		if incremental:
			lt = int(last_tweet[last_tweet["festival"]==festival_id]["last_tweet_id"].iloc[0])
			try:
				tweets = twitter.get_user_timeline(screen_name=festival_id,
												   since_id=lt,
												   exclude_replies=False)
			except TwitterError as e: 
				print(e)
				tweets = twitter.get_user_timeline(screen_name=festival_id,
												   count=200,
												   exclude_replies=False)
		
		else:
			try:
				tweets = twitter.get_user_timeline(screen_name=festival_id,
												   count=200,
												   exclude_replies=False)
			except TwitterError as e: print(e)
		 
		# save last tweet id 
		if len(tweets) > 0:
			last_tweet_id.append(tweets[0]["id"])
		else:
			last_tweet_id.append(lt)
		   
		# save hits
		for t in tweets:
			text = t["text"].lower()
			if any(kb in text for kb in keywords):
				tweet_account_hit.append(festival_id)
				tweet_text_hit.append(t["text"])
				tweet_date_hit.append(t["created_at"])
				tweet_id_hit.append(t["id"])
	
	####### Save info
	# save last tweet				
	pd.DataFrame({'festival':festivals,
				  'last_tweet_id':last_tweet_id}).to_csv("./csv/last_tweet.csv", index=False, encoding='utf-8')
	
	# save last alerts sent
	pd.DataFrame({'festival_id':tweet_account_hit,
				  'tweet_text_hit':tweet_text_hit,
				  'date':tweet_date_hit,
				  'tweet_id':tweet_id_hit}).to_csv("./csv/tweet_hits.csv", index=False)
	
	
	####### Send email
	if len(tweet_text_hit) > 0:
		print("matches found")
		fromaddr = settings.EMAIL_USERNAME
		toaddrs  = settings.EMAIL_TO
		msg = "GIGTAT twitter scan found matches!! :\n\n"
    
		for t in range(len(tweet_text_hit)):
			msg = msg + tweet_account_hit[t] + "\n"
			msg = msg + tweet_text_hit[t] + "\n\n"
			From = fromaddr 
			to = toaddrs 
			subject = 'Gigtat: Twitter hit alert'  
			body = msg
			email_text = """  
			From: %s  
			To: %s  
			Subject: %s

			%s
			""" % (From, to, subject, body)

		# Credentials (if needed) to send email
		username = settings.EMAIL_USERNAME
		password = settings.EMAIL_PASSWORD
		try: 
			# The actual mail send
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.ehlo()
			server.starttls()
			server.login(username,password)
			server.sendmail(fromaddr, toaddrs, email_text)
			server.quit()
        
		except:  
			print ('Something went wrong sending the email')