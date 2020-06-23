import telebot
import telegram_users
from configparser import ConfigParser
from buttons import *
import dadosapi
import requests
import os
import json
from dados_covid import *


config = ConfigParser()
config.read('bot.conf')

TOKEN = config['BRCORONAVIRUSBOT']['TOKEN']

bot = telebot.TeleBot(TOKEN)

botoes = Buttons().botoes
estados = Estados().estados

try:
    cidades = dadosapi.cidadesbr()
    print('Cidades importadas com sucesso!')
except Exception:
    print('Erro! Não foi possível importar as cidades')


def update_graphs_json(all_graphs):
    with open('graphs.json', 'w') as f:
        json.dump(all_graphs, f, ensure_ascii=False)
        return 'Arquivo JSON atualizado!'


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.send_message(chat_id=msg.chat.id,
                     text='Aperte o botão <b>Dados recentes</b> para obter o balanço mais recente'
                     ' de Coronavírus no Brasil\n\n'
                     'Para receber notificações diárias, clique em /cadastrar',
                     reply_markup=botoes,
                     parse_mode='HTML')


@bot.message_handler(commands=['cadastrar'])
def register(msg):
    chatid = msg.chat.id
    userid = msg.from_user.id
    if telegram_users.register(chatid, userid):
        bot.send_message(chat_id=msg.chat.id,
                         text='Usuário cadastrado com sucesso!')
    else:
        bot.send_message(chat_id=msg.chat.id,
                         text='Usuário já está cadastrado.')


@bot.message_handler(func=lambda m: m.text == 'Dados recentes')
def send_brazil_recent_cases(msg):
    titulo = '\U0001F6A8 <b>Dados recentes de Covid-19 no Brasil</b>\n\n'
    cases = dadosapi.brazil_recent_cases()
    footer = '\n\n<b>Ver gráficos:</b> /graficos'
    texto = titulo + cases + footer
    bot.send_message(chat_id=msg.chat.id, text=texto,
                     reply_markup=botoes, parse_mode='HTML')


@bot.message_handler(func=lambda m: m.text == 'Dados por estado')
def send_state_options(msg):
    bot.send_message(chat_id=msg.chat.id,
                     text='<b>Clique no estado desejado</b>\n\n'
                     '<em>Caso não saiba a sigla de um estado, clique em SIGLAS</em>',
                     parse_mode='HTML',
                     reply_markup=estados)


@bot.message_handler(func=lambda m: m.text == 'Dados por cidade')
def send_city_options(msg):
    bot.send_message(chat_id=msg.chat.id,
                     text='Ok! Me envie o nome da cidade (com acentos)\n',
                     parse_mode='HTML')


@bot.message_handler(func=lambda m: m.text.upper() in cidades)
def send_city_recent_cases(msg):
    print(f'Dados por cidade: {msg.text}')
    texto = dadosapi.city_recent_cases(msg.text.strip())
    bot.send_message(chat_id=msg.chat.id,
                     text=texto,
                     parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
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
                              reply_markup=estados)
    else:
        texto = dadosapi.state_recent_cases(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=texto,
                              parse_mode='HTML')


@bot.message_handler(commands=['graficos'])
def send_graphs(msg):
    print(f'{msg.from_user.id} pediu os gráficos')

    graphs_metadata = get_graphs_from_json()
    for filename, metadata in graphs_metadata.items():
        if metadata['id'] is None:
            print('Foto não está no servidor. Uploading...')
            photo = open(f'images/{filename}.png', 'rb')
            
            foto = bot.send_photo(chat_id=msg.chat.id,
                                  photo=photo,
                                  caption=metadata['caption'])
            graphs_metadata[filename]['id'] = foto.photo[0].file_id
            update_graphs_from_json(graphs_metadata)
        else:
            photo = metadata['id']
            foto = bot.send_photo(chat_id=msg.chat.id,
                                  photo=photo,
                                  caption=metadata['caption'])

        print(f'Arquivo <{filename}> enviado')


bot.polling(timeout=60, none_stop=True)
