import yaml
import datetime
from jinja2 import Template, Environment, FileSystemLoader
from google_calendar import GoogleCalendarAPI

# GoogleCalendarAPI の初期化
# 予めcredentials.jsonという名前で認証情報を置いておく必要有
gcapi = GoogleCalendarAPI()
gcapi.auth("credentials.json")

env = Environment(loader=FileSystemLoader('.'), trim_blocks=True)
template = env.get_template("templates/nom_record.md.tpl")

f = open("settings.yaml", "r")
data = yaml.load(f)

for cal in data["Calendars"].keys():
    data["Calendars"][cal]["events"] = {}
    data["Calendars"][cal]["events"]["prev"] = gcapi.get_event(data["Calendars"][cal]["Cals"], datetime.datetime.strptime(data["Start"], "%Y年%m月%d日"), datetime.datetime.strptime(data["End"],"%Y年%m月%d日"))
    data["Calendars"][cal]["events"]["next"] = gcapi.get_event(data["Calendars"][cal]["Cals"], datetime.datetime.strptime(data["Date"], "%Y年%m月%d日"), datetime.datetime.strptime(data["NextDate"],"%Y年%m月%d日"))

disp_text = template.render(data)
print(disp_text)
