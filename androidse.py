#!/usr/bin/python3
# -*- coding: utf-8 -*-

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, Job

token = '517831286:AAHd6UkBKUyRfMHJWamIx59IVMw9j_IPqmI'


updater = Updater(token=token)
dispatcher = updater.dispatcher

def start(bot, update):	  
	bot.sendMessage(chat_id=update.message.chat_id, text="Isto fica feliz em ser útil! \n Estou ajudando o canal @androidse a crescer!!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def welcome(bot, update):
	chat_id = update.message.chat.id
	new_user = update.message.new_chat_members[0].name
	
	bemvindo = "Ei " + new_user + ", que bom te ver por aqui!!!" + "\n" + "Aproveite o espaço, tire suas dúvidas e ajude o crescimento da comunidade!\nNão se esqueça de se inscrever no https://www.meetup.com/pt-BR/android-sergipe/ !"
		
	bot.sendMessage(chat_id=chat_id, text=bemvindo)

welcome_handler = MessageHandler(Filters.status_update.new_chat_members, welcome)
dispatcher.add_handler(welcome_handler)

def git(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="O código deste bot se encontra em http://github.com/arquimago/androidse sinta-se a vontade para fazer seu pull request!")

git_handler = CommandHandler('git', git)
dispatcher.add_handler(git_handler)

updater.start_polling()
