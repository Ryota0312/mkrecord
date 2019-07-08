from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
class Event:
    def __init__(self, summary, description, start, end):
        self.summary = summary
        self.description = description
        self.start = start
        self.end = end

    def __lt__(self, other):
        return self.start < other.start

    @classmethod
    def parse(cls, event):
        summary = event.get("summary")
        description = event.get("description")
        start = event.get("start").get("dateTime")
        end = event.get("end").get("dateTime")
        
        if start == None:
            start = event.get("start").get("date")
            start = datetime.datetime.strptime(start, "%Y-%m-%d")
        else:
            start = datetime.datetime.strptime(start[:19], "%Y-%m-%dT%H:%M:%S")
        if end == None:
            end = event.get("start").get("date")
            end = datetime.datetime.strptime(end, "%Y-%m-%d")
        else:
            end = datetime.datetime.strptime(end[:19], "%Y-%m-%dT%H:%M:%S")            
        
        return Event(summary, description, start, end)

    def print_event(self):
        print(self.summary, self.description, self.start, self.end)

    # %SUMMARY %START %END で出力形式指定
    # timefmtは %STARTと%ENDの日付出力形式
    def fmt(self, fmtstring, timefmt):
        return fmtstring.replace("%SUMMARY", self.summary).replace("%START", datetime.datetime.strftime(self.start, timefmt)).replace("%END", datetime.datetime.strftime(self.start, timefmt))

class GoogleCalendarAPI:
    def __init(self):
        self.credentials = None
        self.service = None

    def auth(self, credential_path):
        self.credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credential_path, SCOPES)
                self.credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)
                
        self.service = build('calendar', 'v3', credentials=self.credentials)

    # calendar_ids で指定したカレンダのイベントを取得し，ソートして返却
    def get_events(self, calendar_ids, start, end):
        # Call the Calendar API
        event_list = []
        for calendar_id in calendar_ids:
            events_result = self.service.events().list(calendarId=calendar_id,
                                                       timeMin=start.isoformat()+'Z',
                                                       timeMax=end.isoformat()+'Z',
                                                       singleEvents=True,
                                                       orderBy='startTime').execute()
            events = events_result.get('items', [])
        
            if not events:
                print('No upcoming events found.')
            for event in events:
                e = Event.parse(event)
                event_list.append(e)

        return sorted(event_list)
