import requests
from lxml import etree




res = requests.get("https://ys.mihoyo.com/main/news/12")
with open("f.txt","w",encoding="utf-8") as f:
    f.write(res.text)