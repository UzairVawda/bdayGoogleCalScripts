# ADD SINGULAR EVENT 
# NO REQUIRED PARAMS
# THE USER IS ASKED A SERIES OF QUESTIONS TO GENERATE ONE EVENT

from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


# ADD YOUR CALENDAR ID HERE
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
	try:      
		service = build('calendar', 'v3', credentials=creds)
		calendarList = service.calendarList().list().execute();
		# calendarList = calendarList.items
		if 'items' in calendarList:
			for index, calendar in enumerate(calendarList['items']):
				print(f"{index + 1}) {calendar['summary']}")
				# print(f"Calendar ID: {calendar['id']}")
				# print("----------")
	except HttpError as error:
		print("Failed Calender Build and Event Fetch")
		print(error)

	calenderId = int(input("Select Calender: ")) - 1
	print(calenderId)
	print(calendarList)
	print(calendarList['items'])
	print(calendarList['items'][calenderId])
	print(calendarList['items'][calenderId]['id'])
	calenderId = calendarList['items'][calenderId]['id']
	print(calenderId)
	title = str(input("Event Title: "))
	duration = int(input("Duration (in minutes): "))
	description = str(input("Event Description: "))
	addEvent(service, calenderId, title, duration, description)


    
# add calendar event from current time for length of 'duration'
def addEvent(service, calenderId, title, duration, description):
	start = datetime.datetime.utcnow()
	end = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(duration))
	start_formatted = start.isoformat() + 'Z'
	end_formatted = end.isoformat() + 'Z'

	event = {
	'summary': title,
	'description': description,
	'start': {
			'dateTime': start_formatted,
			'timeZone': YOUR_TIMEZONE,
			},
	'end': {
			'dateTime': end_formatted,
			'timeZone': YOUR_TIMEZONE,
			},
	}
	event = service.events().insert(calendarId=calenderId, body=event).execute()
	print('Event created: %s' % (event.get('htmlLink')))



if __name__ == '__main__':
    main()
