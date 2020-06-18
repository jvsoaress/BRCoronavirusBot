import telebot
import configparser
import database
import dadosapi

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('bot.conf')

    TOKEN = config['BRCORONAVIRUSBOT']['TOKEN']

    bot = telebot.TeleBot(TOKEN)

    chatid_list = database.notify()
    for chatid in chatid_list:
        titulo = '\U0001F6A8 <b>Dados recentes de Covid-19 no Brasil</b>\n\n'
        cases = dadosapi.brazil_recent_cases()
        footer = '\n\n<b>Ver gráficos:</b> /graficos'
        texto = titulo + cases + footer
        bot.send_message(chat_id=chatid, text=texto, parse_mode='HTML')
