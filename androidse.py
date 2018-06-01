#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, Job, 
from telegram.ext import *
import datetime
import urllib.request, json
import re

arqTokens = open('androidse.token','r')
token = arqTokens.readlines()

for i in range(0,2):
	token[i] = token[i].strip('\n')

arqTokens.close()

token_telegram = token[0]
meetup_token = token[1]

updater = Updater(token=token_telegram)
dispatcher = updater.dispatcher


def start(bot, update):	  
	bot.sendMessage(chat_id=update.message.chat_id, text="Isto fica feliz em ser útil! \n Estou ajudando o canal @androidse a crescer!!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def welcome(bot, update):
	chat_id = update.message.chat.id
	new_user = update.message.new_chat_members[0].name
	
	bemvindo = "Ei " + new_user + ", que bom te ver por aqui!!!" + "\n" + "Aproveite o espaço, tire suas dúvidas e ajude o crescimento da comunidade!"
		
	bot.sendMessage(chat_id=chat_id, text=bemvindo)

welcome_handler = MessageHandler(Filters.status_update.new_chat_members, welcome)
dispatcher.add_handler(welcome_handler)

def git(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="O código deste bot se encontra em http://github.com/arquimago/androidse sinta-se a vontade para fazer seu pull request!")

git_handler = CommandHandler('git', git)
dispatcher.add_handler(git_handler)


def eventos(bot, update):
	url = "https://api.meetup.com/2/events?key="+meetup_token+"&group_urlname=android-sergipe&sign=true"
	url_r = urllib.request.urlopen(url)
	lista_eventos = json.loads(url_r.read().decode())
	eventos = lista_eventos['results']
	resposta = ''
	for evento in eventos:
		nome = '<a href="' + evento['event_url'] + '">'
		nome += "Evento</a>\n" + evento['name'] +'\n\n'
		descricao = evento['description'] +'\n'
		descricao = descricao.replace('<br/>', '\n')
		descricao = re.sub('<[^>]+?>', '', descricao)
		local = "\n<b>Onde?</b> \nLocal:" + evento['venue']['name'] + '\n'
		local += "Endereço: " + evento['venue']['address_1'] + '\n'
		timestamp = evento['time']/1000
		data = datetime.datetime.fromtimestamp(timestamp)
		data_formatada = data.strftime('Dia %d/%m às %H:%M \n')
		resposta = nome + descricao + "\n<b>Quando?</b> \n" + data_formatada + local
	bot.sendMessage(chat_id=update.message.chat_id, text=resposta, parse_mode= "HTML" , disable_web_page_preview=True)

eventos_handler = CommandHandler('eventos', eventos)
dispatcher.add_handler(eventos_handler)


def docs(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Os links para documentos estão disponiveis no https://gist.github.com/arquimago/1c4a3dd775fc8d4fbc0d3e0aa617bb90")

docs_handler = CommandHandler('docs', docs)
dispatcher.add_handler(docs_handler)


updater.start_polling()
