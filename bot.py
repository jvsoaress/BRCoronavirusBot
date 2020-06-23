import telebot
from configparser import ConfigParser
from buttons import *
import dadosapi
import database
import re

config = ConfigParser()
config.read('bot.conf')

TOKEN = config['BRCORONAVIRUSBOT']['TOKEN']

bot = telebot.TeleBot(TOKEN)

try:
    cidades = dadosapi.cidadesbr()
    print('Cidades importadas com sucesso!')
except Exception:
    print('Erro! Não foi possível importar as cidades')

nomes_cidades = list(map(lambda x: x[0], cidades))
repetidas = [(cid, uf) for (cid, uf) in cidades if nomes_cidades.count(cid) > 1]

pattern = re.compile(r'(\*[A-Z]{2})$')


def cidade_repetida(msg):
    lista = []
    retornar = False
    for cid, uf in repetidas:
        if msg.text.upper() == cid:
            cidade = cid
            lista.append(uf)
            retornar = True
    if retornar:
        options = CidadeRepetida(lista, cidade)
        bot.send_message(chat_id=msg.chat.id,
                         text=f'Há {options.cont} municípios com o nome <b>{msg.text.title()}</b>\n',
                         parse_mode='HTML',
                         reply_markup=options.reply_markup)
        return True
    else:
        return False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.id,
                     text='Aperte o botão <b>Dados recentes</b> para obter o balanço mais recente'
                          ' de Coronavírus no Brasil\n\n'
                          'Para receber notificações diárias, clique em /cadastrar',
                     reply_markup=Buttons.botoes,
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
    bot.send_message(chat_id=msg.chat.id, text=texto, reply_markup=Buttons.botoes, parse_mode='HTML')


@bot.message_handler(func=lambda m: m.text == 'Dados por estado')
def send_state_options(msg):
    bot.send_message(chat_id=msg.chat.id,
                     text='<b>Clique no estado desejado</b>\n\n'
                          '<em>Caso não saiba a sigla de um estado, clique em SIGLAS</em>',
                     parse_mode='HTML',
                     reply_markup=Estados.estados)


@bot.message_handler(func=lambda m: m.text == 'Dados por cidade')
def send_city_options(msg):
    bot.send_message(chat_id=msg.chat.id,
                     text='Ok! Me envie o nome da cidade (com acentos)',
                     parse_mode='HTML',
                     reply_markup=t.ForceReply())


@bot.message_handler(func=lambda m: m.reply_to_message)
def send_city_recent_cases(msg):
    if msg.text.upper() in nomes_cidades:
        if not cidade_repetida(msg):
            print(f'Dados por cidade: {msg.text}')
            texto = dadosapi.city_recent_cases(msg.text)
            bot.send_message(chat_id=msg.chat.id,
                             text=texto,
                             parse_mode='HTML',
                             reply_markup=Buttons.botoes)


@bot.callback_query_handler(func=lambda call: '*' not in call.data)
def send_state_recent_cases(call):
    if call.data == 'SIGLAS':
        texto = '<b>Siglas dos estados brasileiros</b>\n\n' \
                'Acre - AC\nAlagoas - AL\nAmapá - AP\nAmazonas - AM\nBahia  - BA\n' \
                'Ceará - CE\nDistrito Federal  - DF\nEspírito Santo - ES\nGoiás - GO\n' \
                'Maranhão - MA\nMato Grosso - MT\nMato Grosso do Sul - MS\nMinas Gerais - MG\n' \
                'Pará - PA\nParaíba - PB\nParaná - PR\nPernambuco - PE\nPiauí - PI\nRio de Janeiro - RJ\n' \
                'Rio Grande do Norte - RN\nRio Grande do Sul - RS\nRondônia - RO\nRoraima - RR\n' \
                'Santa Catarina - SC\nSão Paulo - SP\nSergipe - SE\nTocantins - TO'
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=texto,
                              parse_mode='HTML',
                              reply_markup=Estados.estados)
    else:
        texto = dadosapi.state_recent_cases(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=texto,
                              parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: pattern.search(call.data))
def send_chosen_city_recent_cases(call):
    cidade, estado = call.data.split('*')
    print(f'Dados por cidade repetida: {cidade} ({estado})')
    texto = dadosapi.city_recent_cases(cidade, estado)
    bot.send_message(chat_id=call.message.chat.id,
                     text=texto,
                     parse_mode='HTML',
                     reply_markup=Buttons.botoes)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


bot.polling(timeout=60, none_stop=True)
