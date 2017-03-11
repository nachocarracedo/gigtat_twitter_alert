# twitter keys and tokens API
APP_KEY = ""
APP_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""

# email info
EMAIL_USERNAME = ""
EMAIL_PASSWORD = ""
EMAIL_TO = "" #recipient
SMTP_SERVER = ""

TWITTER_AC_MONITOR = ['@mysteryland', '@MovementDetroit','@nocturnalwland',
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
				
KEYWORDS = ['set time','settime','schedule','timetable','time table'] 

try:
	from private import *
except Exception:
	pass