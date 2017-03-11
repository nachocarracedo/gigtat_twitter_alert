from twython import Twython
import pandas as pd
import settings 
import os.path
import smtplib
import string

if __name__ == "__main__":
	####### Init
	tweet_text_hit= []
	tweet_date_hit= []
	tweet_id_hit = []
	tweet_account_hit = []
	last_tweet_id = []

	# festival twitter accounts
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

	# kewords 
	keywords = ['set time','settime','schedule','timetable','time table']   

	####### twython auth
	twitter = Twython(settings.APP_KEY,
					  settings.APP_SECRET,
					  settings.OAUTH_TOKEN,
					  settings.OAUTH_TOKEN_SECRET)

	####### Incremental search 
	incremental = False
	if os.path.isfile("./csv/last_tweet.csv"):
		last_tweet = pd.read_csv("./csv/last_tweet.csv",encoding='utf-8')
		incremental = True
		
	####### Get and scan tweets 
	for festival_id in festivals:
		if incremental: # get only new tweets since last retreival
			lt = int(last_tweet[last_tweet["festival"]==festival_id]["last_tweet_id"].iloc[0])
			try:
				tweets = twitter.get_user_timeline(screen_name=festival_id,
												   since_id=lt,
												   exclude_replies=True)
			except Exception as e:
					print("***** Error retrieving the tweets ****")
					print(e)
		
		else: # if there is no file ./csv/last_tweet.csv get last 2 tweets
			try:
				tweets = twitter.get_user_timeline(screen_name=festival_id,
												   count=2,
												   exclude_replies=True)
			except Exception as e:
					print("***** Error retrieving the tweets ****")
					print(e)
					
		 
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
				printable = set(string.printable)
				tweet_text_hit.append("".join(list(filter(lambda x: x in printable, t["text"]))))		
				tweet_date_hit.append(t["created_at"])
				tweet_id_hit.append(t["id"])
	
	####### Save info
	# save last tweet				
	pd.DataFrame({'festival':festivals,
				  'last_tweet_id':last_tweet_id}).to_csv("./csv/last_tweet.csv", index=False, encoding='utf-8')
	
	# save alerts sent
	th2 = pd.DataFrame({'festival_id':tweet_account_hit,'tweet_text_hit':tweet_text_hit,'date':tweet_date_hit,'tweet_id':tweet_id_hit})
	if os.path.isfile("./csv/tweet_hits.csv"):
		th1 = pd.read_csv('./csv/tweet_hits.csv')
		pd.concat([th1, th2]).to_csv("./csv/tweet_hits.csv", index=False)
	else:
		th2.to_csv("./csv/tweet_hits.csv", index=False)
	
	####### Send email
	if len(tweet_text_hit) > 0:
		print("Matches found ... ")
		fromaddr = settings.EMAIL_USERNAME
		toaddrs  = settings.EMAIL_TO
		msg = "GIGTAT twitter scan found matches!! :\n\n"
		
		# create email body text
		for t in range(len(tweet_text_hit)):
			msg = msg + tweet_account_hit[t] + " --- " + tweet_date_hit[t] + "\n"
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
			print("Email sent successfully")
        
		except Exception as e:
			print ('Something went wrong sending the email')
			print (e)
	else:
		print("Matches NOT found ... ")