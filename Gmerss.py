# -*- coding: utf-8 -*-
import os
import json
import time
import feedparser

######################################################################################
rssBase={
    "阮一峰":{"url":"http://www.ruanyifeng.com/blog/atom.xml","favicon":"https://www.ruanyifeng.com/favicon.ico","timeFormat":"%Y-%m-%dT%H:%M:%SZ","nameColor":"#bc4c00"},
    "老胡的周刊":{"url":"https://weekly.howie6879.com/rss/rss.xml","favicon":"https://weekly.howie6879.com/statics/images/howie.jpeg","timeFormat":"%a, %d %b %Y %H:%M:%S +0806","nameColor":"#A333D0"},
    "Meekdai":{"url":"https://blog.meekdai.com/rss.xml","favicon":"https://meekdai.com/favicon.svg","timeFormat":"%a, %d %b %Y %H:%M:%S +0000","nameColor":"#1f883d"}
}
displayDay=7
######################################################################################
rssAll=[]
info=json.loads('{}')
info["published"]=int(time.time())
info["rssBase"]=rssBase
rssAll.append(info)

displayTime=info["published"]-displayDay*86400

print("====== Now timestamp = %d ======"%info["published"])
print("====== Start reptile Last %d days ======"%displayDay)

for rss in rssBase:
    print("====== Reptile %s ======"%rss)
    rssDate = feedparser.parse(rssBase[rss]["url"])
    for entry in rssDate['entries']:
        published=int(time.mktime(time.strptime(entry['published'], rssBase[rss]["timeFormat"])))
        if published>displayTime:
            onePost=json.loads('{}')
            onePost["name"]=rss
            onePost["title"]=entry['title']
            onePost["link"]=entry['link']
            onePost["published"]=published
            rssAll.append(onePost)
            print("====== Reptile %s - %s ======"%(rss,onePost["title"]))

print("====== Start sorted %d list ======"%(len(rssAll)-1))
rssAll=sorted(rssAll,key=lambda e:e.__getitem__("published"),reverse=True)

if not os.path.exists('docs/'):
    os.mkdir('docs/')

listFile=open("docs/rssAll.json","w")
listFile.write(json.dumps(rssAll))
listFile.close()
print("====== End reptile ======")
######################################################################################
