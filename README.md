# BRCoronavirusBot
Telegram Bot @BRCoronavirusBot

## About
This is a simple Telegram Bot made to inform about Brazil's Covid-19 spread.

### Sources
- COVID-19 Brazil API, available at https://covid19-brazil-api.now.sh/
- Secretarias de Saúde das Unidades Federativas, data by Álvaro Justen and coworkers, available at https://github.com/turicas/covid19-br/blob/master/api.md
- IBGE locations, available at https://servicodados.ibge.gov.br/api/docs/localidades?versao=1

## Setup
First, create your own virtual environment by typing

<code>virtualenv -p python3 name_of_your_choice</code>

Then, activate it by typing

<code>source ./name_of_your_choice/bin/activate</code>

You're now inside your own virtual environment.
Now install all the required Python packages by typing

<code>pip install -r requirements.txt</code>

Insert your bot TOKEN on <b>sample.conf</b> and rename it to <b>bot.conf</b>.

## Run

First configure your bot. Check [Telegram's API](https://core.telegram.org/bots/api) documentation, section **Authorizing your bot.** You can use [BotFather](https://core.telegram.org/bots#6-botfather) to create your bot's token, which should be add into [bot.conf](https://github.com/bessavagner/BRCoronavirusBot/blob/master/sample.conf).

To start receiving messages just type

<code>python bot.py</code>

#### This is my first bot, and I'm not very experienced to this. 
If you wish to contribute send me a message :)
