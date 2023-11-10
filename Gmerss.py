# -*- coding: utf-8 -*-
import os
import json
import time
import feedparser

######################################################################################
displayDay=7 # 抓取多久前的内容
displayMax=5 # 每个RSS最多抓取数

rssBase={
    "豌豆花下猫":{
        "url":"https://pythoncat.top/rss.xml",
        "favicon":"https://pythoncat.top/favicon.svg",
        "timeFormat":"%a, %d %b %Y %H:%M:%S GMT",
        "nameColor":"#bc4c00"
    },
    "1Link.Fun":{
        "url":"https://1link.fun/index.xml",
        "favicon":"https://fav.farm/🔥",
        "timeFormat":"%a, %d %b %Y %H:%M:%S +0000",
        "nameColor":"#7479dc"
    },
    "阮一峰":{
        "url":"http://www.ruanyifeng.com/blog/atom.xml",
        "favicon":"https://www.ruanyifeng.com/favicon.ico",
        "timeFormat":"%Y-%m-%dT%H:%M:%SZ",
        "nameColor":"#1f883d"
    },
    "老胡的周刊":{
        "url":"https://weekly.howie6879.com/rss/rss.xml",
        "favicon":"https://weekly.howie6879.com/statics/images/howie.jpeg",
        "timeFormat":"%a, %d %b %Y %H:%M:%S +0806",
        "nameColor":"#A333D0"
    },
    "Meekdai":{
        "url":"https://blog.meekdai.com/rss.xml",
        "favicon":"https://meekdai.com/favicon.svg",
        "timeFormat":"%a, %d %b %Y %H:%M:%S +0000",
        "nameColor":"#fd7d7d"
    }
}
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
    i=0
    for entry in rssDate['entries']:
        if i>displayMax:
            break
        published=int(time.mktime(time.strptime(entry['published'], rssBase[rss]["timeFormat"])))
        if published>displayTime:
            onePost=json.loads('{}')
            onePost["name"]=rss
            onePost["title"]=entry['title']
            onePost["link"]=entry['link']
            onePost["published"]=published
            rssAll.append(onePost)
            print("====== Reptile %s - %s ======"%(rss,onePost["title"]))
            i=i+1

print("====== Start sorted %d list ======"%(len(rssAll)-1))
rssAll=sorted(rssAll,key=lambda e:e.__getitem__("published"),reverse=True)

if not os.path.exists('docs/'):
    os.mkdir('docs/')
    print("ERROR Please add docs/index.html")

listFile=open("docs/rssAll.json","w")
listFile.write(json.dumps(rssAll))
listFile.close()
print("====== End reptile ======")
######################################################################################
