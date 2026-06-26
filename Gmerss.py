# -*- coding: utf-8 -*-
import os
import json
import time
import calendar
import feedparser

######################################################################################
displayDay = 7          # 抓取多久前的内容
displayMax = 2          # 每个RSS最多抓取数
weeklyKeyWord = ""      # 周刊过滤关键字

rssBase = {
    "独立开发变现": {
        "url": "https://www.ezindie.com/feed/rss.xml",
        "type": "weekly",
        "nameColor": "#a4244b"
    },
    "夜枫": {
        "url": "https://yefengs.com/feed",
        "type": "post",
        "nameColor": "#b8d101"
    },
    "kn007": {
        "url": "https://kn007.net/feed/",
        "type": "post",
        "nameColor": "#e76976"
    },
    "二丫讲梵": {
        "url": "https://wiki.eryajf.net/learning-weekly.xml",
        "type": "weekly",
        "nameColor": "#93bd76"
    },
    "豌豆花下猫": {
        "url": "https://pythoncat.top/rss.xml",
        "type": "weekly",
        "nameColor": "#bc4c00"
    },
    "阮一峰": {
        "url": "http://www.ruanyifeng.com/blog/atom.xml",
        "type": "weekly",
        "nameColor": "#1f883d"
    },
    "老胡的周刊": {
        "url": "https://weekly.howie6879.com/rss/rss.xml",
        "type": "weekly",
        "nameColor": "#A333D0"
    },
    "Meekdai": {
        "url": "https://blog.meekdai.com/rss.xml",
        "type": "post",
        "nameColor": "#df7150"
    }
}
######################################################################################

rssAll = []

info = {
    "published": int(time.time()),
    "rssBase": rssBase
}

rssAll.append(info)

displayTime = info["published"] - displayDay * 86400

print(f"====== Now timestamp = {info['published']} ======")
print(f"====== Start reptile Last {displayDay} days ======")

for rss, config in rssBase.items():

    print(f"====== Reptile {rss} ======")

    feed = feedparser.parse(config["url"])

    count = 0

    for entry in feed.entries:

        if count >= displayMax:
            break

        # 获取发布时间（兼容 RSS / Atom）
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = calendar.timegm(entry.published_parsed)
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            published = calendar.timegm(entry.updated_parsed)
        else:
            print("Warning: No publish time:", entry.get("title", ""))
            continue

        # 周刊关键字过滤
        if config["type"] == "weekly" and weeklyKeyWord:
            if weeklyKeyWord not in entry.get("title", ""):
                continue

        # 排除未来时间
        if published > info["published"]:
            continue

        # 最近 displayDay 天
        if published > displayTime:

            onePost = {
                "name": rss,
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": published
            }

            rssAll.append(onePost)

            print(f"====== Reptile {onePost['title']} ======")

            count += 1

print(f"====== Start sorted {len(rssAll)-1} list ======")

rssAll.sort(key=lambda x: x["published"], reverse=True)

os.makedirs("docs", exist_ok=True)

with open("docs/rssAll.json", "w", encoding="utf-8") as f:
    json.dump(rssAll, f, ensure_ascii=False, indent=2)

print("====== End reptile ======")
