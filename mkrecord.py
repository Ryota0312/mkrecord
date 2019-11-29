import yaml
import datetime
import sys
import re # for regexp
from jinja2 import Template, Environment, FileSystemLoader
from google_calendar import GoogleCalendarAPI

# 設定ファイル読み込み
args = sys.argv
f = open(args[1], "r")
settings =   yaml.load(f, Loader=yaml.SafeLoader)

# GoogleCalendarAPI の初期化
# 予めcredentials.jsonという名前で認証情報を置いておく必要有
gcapi = GoogleCalendarAPI()
gcapi.auth("credentials.json")

env = Environment(loader=FileSystemLoader('.'), trim_blocks=True)
template = env.get_template(settings["Template"])

# AutoRangeSetFlag == Trueなら，自動でStart, End, Date, NextDateを埋める
# 前後1ヶ月から，MeetingNameに等しい予定の日付を取得し，それが今日以前ならStart，今日以後ならDate，EndはDate - 1, NextDateは，Dateの一月後
today = datetime.datetime.now()
if settings["RangeAutoSetFlag"]:
    start = today.replace(month = today.month -1, day = 1)
    end = today.replace(month = today.month +1, day = 28)
    for cal in settings["Calendars"].keys():
        events = gcapi.get_events(settings["Calendars"][cal]["Ids"], start, end, exclude=settings["MeetingName"])
        for e in events:
            if re.match(settings["MeetingName"], e.summary):
                if today > e.start:
                    settings["Start"] = e.start.strftime("%Y年%m月%d日")
                else:
                    settings["Date"] = e.end.strftime("%Y年%m月%d日")
                    settings["End"] = e.end.replace(day = e.end.day -1).strftime("%Y年%m月%d日")
                    settings["NextDate"] = e.end.replace(month = (e.end.month +1)%12).strftime("%Y年%m月%d日")


# Calendars の各キーについて Ids に含まれるカレンダIDを使ってイベントを取得する
# Calendars.<KEY>.events.prev に Start - End まで
# Calendars.<KEY>.events.next に Date - NextDate まで
for cal in settings["Calendars"].keys():
    settings["Calendars"][cal]["events"] = {}
    settings["Calendars"][cal]["events"]["prev"] = gcapi.get_events(settings["Calendars"][cal]["Ids"], datetime.datetime.strptime(settings["Start"], "%Y年%m月%d日"), datetime.datetime.strptime(settings["End"],"%Y年%m月%d日") + datetime.timedelta(days=1) - datetime.timedelta(seconds=1), settings["Calendars"][cal].get("Filter"), settings["MeetingName"])
    settings["Calendars"][cal]["events"]["next"] = gcapi.get_events(settings["Calendars"][cal]["Ids"], datetime.datetime.strptime(settings["Date"], "%Y年%m月%d日"), datetime.datetime.strptime(settings["NextDate"],"%Y年%m月%d日") + datetime.timedelta(days=1) - datetime.timedelta(seconds=1), settings["Calendars"][cal].get("Filter"), settings["MeetingName"])

## 前回の記録書から項目をコピー
for prev in settings["PrevCopy"].keys():
    f = open(settings["PrevRecord"], "r")
    prev_record = f.read()
    array = re.split('\n', prev_record)
    for v in array:
        if settings["PrevCopy"][prev]["Startline"] in v:
            start_line = array.index(v)
        if settings["PrevCopy"][prev]["Endline"] in v:
            end_line = array.index(v)

    s = ""
    for i in range(start_line + 1, end_line): # 最後の行はいらない
        s += array[i] + "\n"
    settings["PrevCopy"][prev] = s

disp_text = template.render(settings)
print(disp_text)
