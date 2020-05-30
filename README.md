# BRCoronavirusBot
Telegram Bot @BRCoronavirusBot

##About
This is a simple Telegram Bot made to inform about Brazil's Covid-19 spread.

##Setup
First, create your own virtual environment by typing

<code>virtualenv -p python3 name_of_your_choice</code>

Then, activate it by typing

<code>source ./name_of_your_choice/bin/activate</code>

You're now inside your own virtual environment.
Now install all the required Python packages by typing

<code>pip install -r requirements.txt</code>

Insert your bot TOKEN on <code>sample.conf</code> and rename it to <code>bot.conf</code>.

Create a file <code>users.csv</code> with headers <code>chatid,userid</code> to receive data when someone registers.
##Run

To start receiving messages just type

<code>python bot.py</code>

####This is my first bot, and I'm not very experienced to this. 
If you wish to contribute send me a message :)