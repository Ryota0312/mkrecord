from __future__ import print_function
import datetime
import pickle
import os.path
import re
import sys
from abc import ABCMeta
from abc import abstractmethod
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class EventCollection:
    def __init__(self, events=None):
        if events == None:
            self.events = []
        else:
            self.events = events

    def __getitem__(self, key):
        return self.events[key]

    @classmethod
    def parse(cls, google_events, filters=None, exclude=None):
        if exclude == None: exclude = []
        # 同じsummaryの予定をグルーピング
        # exclude に指定した予定はグルーピングしない
        # TODO: 現在，excludeにはMeetingNameのみ指定しているが，設定ファイルから設定したい
        sorted_events = sorted(google_events, key=lambda x:x["summary"])
        grouped_events = []
        grouping_index = 0
        if len(sorted_events)==0: return EventCollection([])
        prev_event = sorted_events[grouping_index]
        for i,event in enumerate(sorted_events):
            if i==0: continue
            if (event["summary"]==prev_event["summary"]) and (not re.match(exclude, event["summary"])):
                pass
            else:
                grouped_events.append(sorted_events[grouping_index:i])
                grouping_index = i
            prev_event = sorted_events[i]
        grouped_events.append(sorted_events[grouping_index:-1])

        events = []
        for event in grouped_events:
            # filters に指定した正規表現にマッチしないものは無視
            if filters:
                if filters.get("summary"):
                    if re.search(filters["summary"], event[0]["summary"]) == None: continue
                if filters.get("description"):
                    if re.search(filters["description"], event[0]["description"]) == None: continue
            if len(event) == 1:
                e = SingleEvent.parse(event[0])
                events.append(e)
            elif len(event) > 1:
                e = RepetitionEvent.parse(event)
                events.append(e)

        return EventCollection(events)

    def merge(self, event_collection):
        self.events += event_collection.events

    def append(self, event):
        self.events.append(event)

    def sort(self):
        self.events =  sorted(self.events)
    
class Event(metaclass = ABCMeta):
    @classmethod
    @abstractmethod
    def parse(cls, event):
        pass

    @abstractmethod
    def fmt(self, fmtstring, timefmt):
        pass

class RepetitionEvent(Event):
    def __init__(self, summary, description, start, end):
        if (type(summary) != list) or (type(description) != list) or (type(start) != list) or (type(end) != list): raise TypeError
        # リスト
        self.summary_list = summary
        self.description_list = description
        self.start_list = start
        self.end_list = end
        # 1つ目の予定を代表値として使っている
        # TODO: ちょっときもいから綺麗にしたい
        self.summary = self.summary_list[0]
        self.description = self.description_list[0]
        self.start = self.start_list[0]
        self.end = self.end_list[0]

    def __lt__(self, other):
        return self.start < other.start

    def __getitem__(self, key):
        return SingleEvent(self.summary_list[key], self.description_list[key], self.start_list[key], self.end_list[key])

    @classmethod
    def parse(cls, events):
        summary = []
        description = []
        start = []
        end = []
        for event in events:
            summary.append(event.get("summary"))
            description.append(event.get("description"))
            s = event.get("start").get("dateTime")
            e = event.get("end").get("dateTime")
        
            if s == None:
                s = event.get("start").get("date")
                s = datetime.datetime.strptime(s, "%Y-%m-%d")
            else:
                s = datetime.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
            if e == None:
                e = event.get("start").get("date")
                e = datetime.datetime.strptime(e, "%Y-%m-%d")
            else:
                e = datetime.datetime.strptime(e[:19], "%Y-%m-%dT%H:%M:%S")

            start.append(s)
            end.append(e)
        
        return RepetitionEvent(summary, description, start, end)

    # %SUMMARY %START %END で出力形式指定
    # timefmtは %STARTと%ENDの日付出力形式
    def fmt(self, fmtstring, timefmt):
        return fmtstring.replace("%SUMMARY", self.summary).replace("%START", ",".join([datetime.datetime.strftime(x, timefmt) for x in self.start_list])).replace("%END", ",".join([datetime.datetime.strftime(x, timefmt) for x in self.end_list]))

class SingleEvent(Event):
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
        
        return SingleEvent(summary, description, start, end)

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
    def get_events(self, calendar_ids, start, end, filters=None, exclude=None):
        # Call the Calendar API
        event_list = EventCollection()
        for calendar_id in calendar_ids:
            events_result = self.service.events().list(calendarId=calendar_id,
                                                       timeMin=start.isoformat()+'+09:00',
                                                       timeMax=end.isoformat()+'+09:00',
                                                       singleEvents=True,
                                                       orderBy='startTime').execute()
            events = events_result.get('items', [])

            event_list_each_cal = EventCollection.parse(events, filters, exclude)
            event_list.merge(event_list_each_cal)

        event_list.sort()
        return event_list
