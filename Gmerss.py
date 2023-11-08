# -*- coding: utf-8 -*-
import os
import json
import time
import feedparser

######################################################################################
rssBase=[
    {"name":"Meekdai","url":"https://blog.meekdai.com/rss.xml","favicon":"https://meekdai.com/favicon.svg","timeFormat":"%a, %d %b %Y %H:%M:%S +0000","nameColor":"#1f883d"},
    {"name":"老胡的周刊","url":"https://weekly.howie6879.com/rss/rss.xml","favicon":"https://weekly.howie6879.com/statics/images/howie.jpeg","timeFormat":"%a, %d %b %Y %H:%M:%S +0806","nameColor":"#A333D0"}
]
######################################################################################

for rss in rssBase:
    rssDate = feedparser.parse(rss["url"])
    rss["list"] = [{'title': entry['title'], 'link':entry['link'], 'published':time.mktime(time.strptime(entry['published'], rss["timeFormat"]))} for entry in rssDate['entries']] 


listFile=open("rssBase.json","w")
listFile.write(json.dumps(rssBase))
listFile.close()
#目前list排列需要在python进行
######################################################################################
