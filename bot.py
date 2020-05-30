import telebot
from configparser import ConfigParser
from telebot import types as t
import dadosapi
import database
from time import sleep

config = ConfigParser()
config.read('bot.conf')

TOKEN = config['BRCORONAVIRUSBOT']['TEST_TOKEN']

bot = telebot.TeleBot(TOKEN)

botoes = t.ReplyKeyboardMarkup(row_width=1)
botao1 = t.KeyboardButton('Dados recentes')
botao2 = t.KeyboardButton('Dados por estado')
botoes.add(botao1, botao2)

estados = t.InlineKeyboardMarkup()
sp = t.KeyboardButton('SP')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.id,
                     text='Aperte o botão <b>Dados recentes</b> para obter o balanço mais recente'
                          ' de Coronavírus no Brasil.\n\n'
                          'Para receber notificações diárias, clique em /cadastrar',
                     reply_markup=botoes,
                     parse_mode='HTML')


@bot.message_handler(commands=['cadastrar'])
def register(msg):
    chatid = msg.chat.id
    userid = msg.from_user.id
    if database.register(chatid, userid):
        bot.send_message(chat_id=msg.chat.id, text='Usuário cadastrado com sucesso!')
    else:
        bot.send_message(chat_id=msg.chat.id, text='Usuário já está cadastrado.')


@bot.message_handler(func=lambda m: m.text == 'Dados recentes')
def send_brazil_recent_cases(msg):
    titulo = '\U0001F6A8 <b>Dados recentes de Covid-19 no Brasil</b>\n\n'
    cases = dadosapi.brazil_recent_cases()
    texto = titulo + cases
    bot.send_message(chat_id=msg.chat.id, text=texto, reply_markup=botoes, parse_mode='HTML')


@bot.message_handler(func=lambda m: m.text == 'Por estado')
def send_state_options(msg):
    bot.send_message(chat_id=msg.chat.id,
                     text='<b>Clique no estado desejado</b>\n\n'
                          '<em>Caso não saiba a sigla de um estado, clique em MOSTRAR SIGLAS</em>',
                     parse_mode='HTML',
                     reply_markup=estados)


try:
    bot.polling(timeout=20, none_stop=True)
except Exception:
    print('Telegram API connection error. Waiting 30 seconds.')
    sleep(30)
