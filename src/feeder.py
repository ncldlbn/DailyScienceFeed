#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
import sqlite3
import telegram
from telegram import ParseMode
from datetime import datetime

# path to this repo
path = "C:/Users/nicol/OneDrive/Documenti/Projects/DailyScienceFeed/"
# database offerte già inviate
database = path + "data/feed.db"
# token e id bot telegram
bot_data = path + "data/bot.txt"

bot_info = open(bot_data,"r")
bot_token = bot_info.readline().strip('\n')
bot_id = bot_info.readline().strip('\n')

# Creazione del client Telegram
bot = telegram.Bot(token=bot_token)

db = sqlite3.connect(database)
c = db.cursor()
# rimuovi news più vecchie di x giorni (da implementare!!)
# seleziona la tabella delle news già inviate
c.execute('SELECT Title FROM old')
old = c.fetchall()
old = [result[0] for result in old]
# seleziona la lista di url da cui ricavare i feeds
c.execute('SELECT url FROM feeds')
url = c.fetchall()
urls = [result[0] for result in url]
db.commit()
db.close()

for u in urls:
    feed = feedparser.parse(u)
    topic = feed.feed.title.split(' News ')[0]
    news = []
    for entry in feed.entries:
        title = entry.title
        description = entry.description
        link = entry.link
        date = entry.published
        if date is not None:
            date = date.split(' ')[0] + ' ' + date.split(' ')[1] + ' ' + date.split(' ')[2] + ' ' + date.split(' ')[3]
            date = datetime.strptime(date, '%a, %d %b %Y')
            date = date.strftime('%d-%m-%Y')
        if title not in old:
            db = sqlite3.connect(database)
            c = db.cursor()
            c.execute('INSERT INTO old (Topic, Title, Link, PubDate) VALUES (?, ?, ?, ?)',
                      (topic, title, link, date))
            db.commit()
            db.close()
            
            # invia messaggio
            link_title = "<a " + "href='" + link + "'>" + title + "</a>"
            message = topic + "\n\n" + link_title + "\n\n" + description

            bot.send_message(chat_id=bot_id, text=message, disable_web_page_preview=True, parse_mode = ParseMode.HTML)

