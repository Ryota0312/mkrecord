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


# Calendars の各キーについて Ids に含まれるカレンダIDを使ってイベントを取得する
# Calendars.<KEY>.events.prev に Start - End まで
# Calendars.<KEY>.events.next に Date - NextDate まで
for cal in settings["Calendars"].keys():
    settings["Calendars"][cal]["events"] = {}
    settings["Calendars"][cal]["events"]["prev"] = gcapi.get_events(settings["Calendars"][cal]["Ids"], datetime.datetime.strptime(settings["Start"], "%Y年%m月%d日"), datetime.datetime.strptime(settings["End"],"%Y年%m月%d日") + datetime.timedelta(days=1) - datetime.timedelta(seconds=1), settings["Calendars"][cal].get("Filter"))
    settings["Calendars"][cal]["events"]["next"] = gcapi.get_events(settings["Calendars"][cal]["Ids"], datetime.datetime.strptime(settings["Date"], "%Y年%m月%d日"), datetime.datetime.strptime(settings["NextDate"],"%Y年%m月%d日") + datetime.timedelta(days=1) - datetime.timedelta(seconds=1), settings["Calendars"][cal].get("Filter"))

f = open(settings["OldRecord"], "r")
old_record = f.read()
array = re.split('\n', old_record)
for v in array:
    if "研究関連" in v:
        start_line = array.index(v)
    if "研究室関連" in v:
        end_line = array.index(v) # 最初の「研究室関連」だけほしいので，enumerateではなくindexを使う

s = ""
for i in range(start_line + 1, end_line): # 「研究関連」の一文はいらないので一つずらす
    s += array[i] + "\n"
settings["Research"] = s

disp_text = template.render(settings)
print(disp_text)
