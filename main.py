from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]


user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_xingzuo():
  xingzuo = requests.get("http://web.juhe.cn/constellation/getAll?consName=%E6%B0%B4%E7%93%B6%E5%BA%A7&type=today&key=5d4c067629b359a72ee6c0c2008ccf3d")
  return xingzuo.json()['summary']
def get_xingzuo1(x):
  xingzuo = requests.get("http://web.juhe.cn/constellation/getAll?consName=%E6%B0%B4%E7%93%B6%E5%BA%A7&type=today&key=5d4c067629b359a72ee6c0c2008ccf3d")
  return xingzuo.json()[x]

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {'QFriend':{'value':get_xingzuo1('QFriend')},'number':{'value':get_xingzuo1('number')},'money':{'value':get_xingzuo1('money')},'work':{'value':get_xingzuo1('work')},'love':{'value':get_xingzuo1('love')},'health':{'value':get_xingzuo1('health')},'luckycolor':{'value':get_xingzuo1('color')},"summary":{'value':get_xingzuo(), "color":get_random_color()},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
