'''
Patrick
3/13/2024
'''
from datetime import datetime, timedelta
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
from helper import time_conversion

SCOPES = ['https://www.googleapis.com/auth/calendar']


def gcal_event_creation(location, participants, startDateTime, endDateTime, tennisCalendarId):
    '''
    Creates a Google Calendar event using provided parameters.

    Parameters:
        location (str): A string representing the courts being played on.
        participants (str): A string representing the participants playing.
        startDateTime (str): A string representing the start date and time.
        endDateTime (str): A string representing the end date and time.
        tennisCalendarId (string): A string representing the ID of the associated calendar

    Returns:
        None
    '''
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": "Tennis with " + participants, 
            "location": location,
            "description": participants, 
            "color": 6,
            "start": {
                "dateTime":startDateTime,
                "timeZone":"America/Toronto"
            },
            "end": {
                "dateTime":endDateTime,
                "timeZone":"America/Toronto"
            },
        }

        event = service.events().insert(calendarId=tennisCalendarId, body=event).execute()

        print(f"Event created {event.get('htmlLink')}")
    except HttpError as error:
        print("An error occurred:", error)



def delete_event(eventsToDelete, tennisCalendarId):
    '''
    Deletes Google Calendar events corresponding to the provided tennis event information.

    Parameters:
        eventsToDelete (dictionary): A dictionary containing information of a single tennis event set to be deleted.
        tennisCalendarId (string): A string representing the ID of the associated calendar
        
    Returns:
        None
    '''
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    try:
        minDateTimeObj = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
        formattedMinDatetime = minDateTimeObj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        maxDateTimeObj = datetime.strptime(str(datetime.now()+ timedelta(days=30)), "%Y-%m-%d %H:%M:%S.%f")
        formattedMaxDatetime = maxDateTimeObj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        service = build("calendar", "v3", credentials=creds)
        events =  events = service.events().list(
            calendarId=tennisCalendarId,
            timeMin=formattedMinDatetime,
            timeMax=formattedMaxDatetime,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        for event in events['items']:
            # Iterating through the listed tennis events
            # Check if participants the same, then check if date/time if the same, if so delete the event
            pattern = re.compile(r'\bwith \b(.*)')
            extracted_participants = pattern.search(event['summary'])
            # Check if time is identical
            convertedTime = time_conversion(eventsToDelete.get('Date and Time'))
            currentEventStart = event['start'].get('dateTime')[:19]
            currentEventEnd = event['end'].get('dateTime')[:19]
            deleteEventStart = convertedTime[0]
            deleteEventEnd = convertedTime[1]
            if extracted_participants.group(1) == eventsToDelete.get('Participants'):
                if currentEventStart == deleteEventStart:
                    if currentEventEnd == deleteEventEnd:
                        service.events().delete(calendarId=tennisCalendarId, eventId=event['id']).execute()
    except HttpError as error:
        print(error)
