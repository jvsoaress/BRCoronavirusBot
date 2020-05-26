import telebot
from configparser import ConfigParser
from telebot import types as t
import dados

config = ConfigParser()
config.read('bot.conf')

TOKEN = config['BRCORONAVIRUSBOT']['TOKEN']

bot = telebot.TeleBot(TOKEN)

botoes = t.ReplyKeyboardMarkup()
botao1 = t.KeyboardButton('Dados recentes')
botoes.add(botao1)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.id, text='Olá!', reply_markup=botoes)


@bot.message_handler(func=lambda m: m.text == 'Dados recentes')
def send_recent_data(msg):
    data = dados.send_recent_data()
    bot.send_message(chat_id=msg.chat.id, text=data, reply_markup=botoes)


bot.polling(timeout=20, none_stop=True)