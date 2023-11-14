# -*- coding: utf-8 -*-
import os
import json
import time
import feedparser

######################################################################################
displayDay=7 # 抓取多久前的内容
displayMax=2 # 每个RSS最多抓取数
weeklyKeyWord="" # 周刊过滤关键字

rssBase={
    "独立开发变现":{
        "url":"https://www.ezindie.com/feed/rss.xml",
        "type":"weekly",
        "timeFormat":"%a, %d %b %Y %H:%M:%S GMT",
        "nameColor":"#a4244b"
    },
    "夜枫":{
        "url":"https://yefengs.com/feed",
        "type":"post",
        "timeFormat":"%a, %d %b %Y %H:%M:%S +0000",
        "nameColor":"#b8d101"
    },
    "kn007":{
        "url":"https://kn007.net/feed/",
        "type":"post",
        "timeFormat":"%a, %d %b %Y %H:%M:%S +0000",
        "nameColor":"#e76976"
    },
    "二丫讲梵":{
        "url":"https://wiki.eryajf.net/learning-weekly.xml",
        "type":"weekly",
        "timeFormat":"%a, %d %b %Y %H:%M:%S +0800",
        "nameColor":"#93bd76"
    },
    "豌豆花下猫":{
        "url":"https://pythoncat.top/rss.xml",
        "type":"weekly",
        "timeFormat":"%a, %d %b %Y %H:%M:%S GMT",
        "nameColor":"#bc4c00"
    },
    "1Link":{
        "url":"https://1link.fun/index.xml",
        "type":"weekly",
        "timeFormat":"%a, %d %b %Y %H:%M:%S +0000",
        "nameColor":"#7479dc"
    },
    "阮一峰":{
        "url":"http://www.ruanyifeng.com/blog/atom.xml",
        "type":"weekly",
        "timeFormat":"%Y-%m-%dT%H:%M:%SZ",
        "nameColor":"#1f883d"
    },
    "老胡的周刊":{
        "url":"https://weekly.howie6879.com/rss/rss.xml",
        "type":"weekly",
        "timeFormat":"%a, %d %b %Y %H:%M:%S +0806",
        "nameColor":"#A333D0"
    },
    "Meekdai":{
        "url":"https://blog.meekdai.com/rss.xml",
        "type":"post",
        "timeFormat":"%a, %d %b %Y %H:%M:%S +0000",
        "nameColor":"#df7150"
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
        if i>=displayMax:
            break
        published=int(time.mktime(time.strptime(entry['published'], rssBase[rss]["timeFormat"])))

        if entry['published'][-5]=="+":
            published=published-(int(entry['published'][-5:])*36)

        if rssBase[rss]["type"]=="weekly" and (weeklyKeyWord not in entry['title']):
            continue

        if published>info["published"]:
            continue

        if published>displayTime:
            onePost=json.loads('{}')
            onePost["name"]=rss
            onePost["title"]=entry['title']
            onePost["link"]=entry['link']
            onePost["published"]=published
            rssAll.append(onePost)
            print("====== Reptile %s ======"%(onePost["title"]))
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
