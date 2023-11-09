# -*- coding: utf-8 -*-
import os
import json
import time
import feedparser

######################################################################################
rssBase={
    "Meekdai":{"url":"https://blog.meekdai.com/rss.xml","favicon":"https://meekdai.com/favicon.svg","timeFormat":"%a, %d %b %Y %H:%M:%S +0000","nameColor":"#1f883d"},
    "老胡的周刊":{"url":"https://weekly.howie6879.com/rss/rss.xml","favicon":"https://weekly.howie6879.com/statics/images/howie.jpeg","timeFormat":"%a, %d %b %Y %H:%M:%S +0806","nameColor":"#A333D0"}
}
######################################################################################
rssAll=[]
info=json.loads('{}')
info["published"]=int(time.time())
info["rssBase"]=rssBase
rssAll.append(info)

for rss in rssBase:
    rssDate = feedparser.parse(rssBase[rss]["url"])
    # onePost = [{'title': entry['title'], 'link':entry['link'], 'published':time.mktime(time.strptime(entry['published'], rss["timeFormat"]))} for entry in rssDate['entries']] 
    for entry in rssDate['entries']:
        onePost=json.loads('{}')
        onePost["name"]=rss
        onePost["title"]=entry['title']
        onePost["link"]=entry['link']
        onePost["published"]=time.mktime(time.strptime(entry['published'], rssBase[rss]["timeFormat"]))
        rssAll.append(onePost)

rssAll=sorted(rssAll,key=lambda e:e.__getitem__("published"),reverse=True)

listFile=open("rssAll.json","w")
listFile.write(json.dumps(rssAll))
listFile.close()
#需要配置展示一周还是几天
######################################################################################
