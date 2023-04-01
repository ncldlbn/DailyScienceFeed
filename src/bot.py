#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import telegram
import sqlite3
from telegram.ext import Updater, CommandHandler
from feeder import feeder

# path to this repo
path = "/home/nicola/Projects/DailyScienceFeed/"
# database offerte già inviate
database = path + "data/feed.db"


def send_news(bot):

    # Parsa il feed RSS
    news = feeder(database)

    # Manda un messaggio su Telegram per ogni news
    for n in news:
        
        
# # Comando per aggiungere un nuovo feed
# def add_feed(update, context):
#     # Ottieni il feed da aggiungere dal messaggio dell'utente
#     new_feed = context.args[0]

#     # Aggiungi il nuovo feed alla lista dei feed
#     db = sqlite3.connect(database)
#     c = db.cursor()
#     c.execute('INSERT INTO feeds (url) VALUES (?)', (new_feed))
#     db.commit()
#     db.close()

#     # Invia un messaggio di conferma all'utente
#     bot.send_message(chat_id=chat_id, text="Nuovo feed aggiunto!")

# # Comando per rimuovere un feed esistente
# def remove_feed(update, context):
#     # Ottieni il feed da rimuovere dal messaggio dell'utente
#     old_feed = context.args[0]

#     # Rimuovi il feed dalla lista dei feed
#     db = sqlite3.connect(database)
#     c = db.cursor()
#     c.execute('DELETE FROM feeds (url) VALUES (?)', (old_feed))
#     db.commit()
#     db.close()

#     # Invia un messaggio di conferma all'utente
#     bot.send_message(chat_id=chat_id, text="Feed rimosso!")


# Aggiungi i gestori dei comandi al dispatcher del bot
updater = Updater(bot_token, use_context=True)
#updater.dispatcher.add_handler(CommandHandler('add_feed', add_feed))
#updater.dispatcher.add_handler(CommandHandler('remove_feed', remove_feed))

# Crea un oggetto JobQueue e passa l'Updater
job_queue = updater.job_queue
# Aggiungi la funzione send_news alla JobQueue
job_queue.run_repeating(send_news, interval=10, first=0)


# Avvia il bot
updater.start_polling()
updater.idle()