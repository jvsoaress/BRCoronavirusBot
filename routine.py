import telebot
import configparser
import telegram_users
from dados_covid import brazil_recent_cases

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('bot.conf')

    TOKEN = config['BRCORONAVIRUSBOT']['TOKEN']

    bot = telebot.TeleBot(TOKEN)

    chatid_list = telegram_users.notify()
    for chatid in chatid_list:
        texto = brazil_recent_cases()
        bot.send_message(chat_id=chatid, text=texto, parse_mode='HTML')
