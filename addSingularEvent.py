# ADD SINGULAR EVENT 
# REQUIRED PARAMS
# ADD -> currently add only
# DURATION -> how long the event is scheduled for  
# TITLE -> event title 



from __future__ import print_function

import datetime
import os.path
from sys import argv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


# ADD YOUR CALENDAR ID HERE
YOUR_CALENDAR_ID = 'uzair.vawda@gmail.com'
YOUR_TIMEZONE = 'GMT-5' # find yours here: https://www.timezoneconverter.com/cgi-bin/zonehelp.tzc?cc=US&ccdesc=United%20States


def main():
	creds = None

	if os.path.exists('token.json'):
			creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
					creds.refresh(Request())
			else:
					flow = InstalledAppFlow.from_client_secrets_file(
							'credentials.json', SCOPES)
					creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open('token.json', 'w') as token:
					token.write(creds.to_json())

	# determine which function to run        
	if argv[1] == 'add':
		duration = argv[2]
		description = argv[3]
		addEvent(creds, duration, description)
	else:
		print("THIS IS AN ADD ONLY FUNCTION")
		return

    
# add calendar event from curret time for length of 'duration'
def addEvent(creds, duration, description):
	start = datetime.datetime.utcnow()
	
	end = datetime.datetime.utcnow() + datetime.timedelta(hours=int(duration))
	start_formatted = start.isoformat() + 'Z'
	end_formatted = end.isoformat() + 'Z'

	event = {
	'summary': description,
	'start': {
			'dateTime': start_formatted,
			'timeZone': YOUR_TIMEZONE,
			},
	'end': {
			'dateTime': end_formatted,
			'timeZone': YOUR_TIMEZONE,
			},
	}
	print(event)

	service = build('calendar', 'v3', credentials=creds)
	print(service)

	event = service.events().insert(calendarId=YOUR_CALENDAR_ID, body=event).execute()
	print(event)

	print('Event created: %s' % (event.get('htmlLink')))



if __name__ == '__main__':
    main()
