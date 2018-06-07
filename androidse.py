#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import randint
from telegram.ext import *
import datetime
import urllib.request, json
import re

arqTokens = open('androidse.token','r')
token = arqTokens.readlines()
arqTokens.close()

for i in range(0,2):
	token[i] = token[i].strip('\n')

token_telegram = token[0]
meetup_token = token[1]

arqAdmins = open('admins.token','r')
admins = arqAdmins.readlines()
arqAdmins.close()

chatAdmins = -1001315295672
chatPrincipal = "@AndroidSE"

for i in range(0,len(admins)):
	admins[i] = admins[i].strip('\n')

arqLinguagens = open('linguagens.txt','r')
linguagens = arqLinguagens.readlines()
arqLinguagens.close()

for i in range(0,len(linguagens)):
	linguagens[i] = linguagens[i].strip('\n')

def start(bot, update):	  
	bot.sendMessage(chat_id=update.message.chat_id, text="Isto fica feliz em ser útil! \n Estou ajudando o canal @androidse a crescer!!")

def welcome(bot, update):
	chat_id = update.message.chat.id
	new_user = update.message.new_chat_members[0].name
	bemvindo = "Ei " + new_user + ", que bom te ver por aqui!!!" + "\n" + "Aproveite o espaço, tire suas dúvidas e ajude o crescimento da comunidade!"
	bot.sendMessage(chat_id=chat_id, text=bemvindo)

def git(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="O código deste bot se encontra em http://github.com/arquimago/androidse sinta-se a vontade para fazer seu pull request!")

def eventos(bot, update):
	url = "https://api.meetup.com/2/events?key="+meetup_token+"&group_urlname=android-sergipe&sign=true"
	url_r = urllib.request.urlopen(url)
	lista_eventos = json.loads(url_r.read().decode())
	eventos = lista_eventos['results']
	resposta = ''
	for evento in eventos:
		nome = '<a href="' + evento['event_url'] + '">'
		nome += "Evento: " + evento['name'] +'</a>\n\n'
		descricao = evento['description'] +'\n'
		descricao = descricao.replace('<br/>', '\n')
		descricao = re.sub('<[^>]+?>', '', descricao)
		try:
			local = "\n<b>Onde?</b> \nLocal: " + evento['venue']['name'] + '\n' + "Endereço: " + evento['venue']['address_1'] + '\n'
		except KeyError:
			local = "\n<b>Sem Local Definido</b>\n"
		timestamp = evento['time']/1000
		data = datetime.datetime.fromtimestamp(timestamp)
		data_formatada = data.strftime('Dia %d/%m às %H:%M \n')
		resposta += nome + descricao + "\n<b>Quando?</b> \n" + data_formatada + local + "\n"
	bot.sendMessage(chat_id=update.message.chat_id, text=resposta, parse_mode= "HTML" , disable_web_page_preview=True)

def help(bot, update):
	texto = "Isto fica feliz em ser útil!\n"
	texto += "Use os comandos abaixo para interagir com o bot\n"
	texto += "/start - Inicia o bot\n"
	texto += "/help - Mostra esta lista de comandos\n"
	texto += "/git - Retorna o repositório do bot no github\n"
	texto += "/eventos - Lista os próximos eventos do Meetup\n"
	texto += "/docs - Envia o link com os links para documentos de eventos passados\n"
	texto += "/querocontribuir - Use este comando se quiser contribuir com a comunidade!\n"
	bot.sendMessage(chat_id=update.message.chat_id, text=texto)

def docs(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Os links para documentos estão disponiveis no https://gist.github.com/arquimago/1c4a3dd775fc8d4fbc0d3e0aa617bb90")

def querocontribuir(bot, update):
	nome = update.message.from_user.username
	if nome in admins:
		texto = "Hey @"+nome+", você sabe exatamente o que fazer para contribuir né?"
		bot.sendMessage(chat_id=chatAdmins, text=texto)
	else:
		texto = "Olá "+nome+" que bom que você tem interesse em contribuir!\n Entraremos em contato em breve!"
		bot.sendMessage(chat_id=update.message.chat_id, text=texto)
		texto = "Alô Galera!! Fiquem atentos! <b>"+nome+"</b> quer ajudar no crescimento da comunidade!"
		bot.sendMessage(chat_id=chatAdmins, text=texto, parse_mode="HTML")

def conversas(bot, update):
	chat_id = update.message.chat.id
	frase = update.message.text.lower()
	nome = update.message.from_user.username
	comando = update.message.text.split()[0].lower()
	sorteio = randint(0,100)
	print(sorteio)
	if (chat_id == chatAdmins or nome in admins) and comando == ".anuncio":
		msg = update.message.text.split()
		msg.remove(".anuncio")
		msg = " ".join(msg)
		texto = "<b>ANUNCIO:</b>\n" + msg
		if(len(texto.split()) < 4):
			bot.sendMessage(chat_id=chat_id, text="Anuncio muito curto!!")
		else:
			bot.sendMessage(chat_id=chatPrincipal, text=texto, parse_mode= "HTML")
			bot.sendMessage(chat_id=chatAdmins, text="Anucio feito com sucesso!")
	elif (chat_id == chatAdmins or nome in admins) and comando == ".zoeira":
		texto = update.message.text.split()
		texto.remove(".zoeira")
		texto = " ".join(texto)
		print(texto)
		bot.sendMessage(chat_id=chatPrincipal, text=texto, parse_mode= "HTML")
		bot.sendMessage(chat_id=chat_id, text="Eu amo a zoeira!")
	elif sorteio<20:
		print("entrou")
		for l in linguagens:
			if l in frase:
				arquivo = l+".txt"
				arqRespostas = open(arquivo,'r')		
				respostas = arqRespostas.readlines()
				arqRespostas.close()
				print("ate ja leu o arquivo")
				for i in range(0,len(respostas)):
					respostas[i] = respostas[i].strip('\n')
				resposta = respostas[randint(0,len(respostas))]
				prompt = "o bot falou de "+ l + "porque tirou um "+ sorteio+" no dado"
				print(prompt)
				break
		bot.sendMessage(chat_id=chat_id, text=resposta)

def main():
	updater = Updater(token=token_telegram)
	dispatcher = updater.dispatcher
	
	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)

	git_handler = CommandHandler('git', git)
	dispatcher.add_handler(git_handler)

	eventos_handler = CommandHandler('eventos', eventos)
	dispatcher.add_handler(eventos_handler)

	help_handler = CommandHandler('help', help)
	dispatcher.add_handler(help_handler)

	docs_handler = CommandHandler('docs', docs)
	dispatcher.add_handler(docs_handler)

	querocontribuir_handler = CommandHandler('querocontribuir', querocontribuir)
	dispatcher.add_handler(querocontribuir_handler)

	conversas_handler = MessageHandler(Filters.text, conversas)
	updater.dispatcher.add_handler(conversas_handler)

	#Função de boas vindas, desativada pra evitar flood
	#welcome_handler = MessageHandler(Filters.status_update.new_chat_members, welcome)
	#dispatcher.add_handler(welcome_handler)

	updater.start_polling()

if __name__ == '__main__':
	main()
