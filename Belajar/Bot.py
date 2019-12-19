import telebot, time, os
from telebot import types
from app.rules import inlineForWali
from config import conf, text_messages
import flask

app = flask.Flask(__name__)

BOT_TOKEN = '{}'.format(conf['token'])
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

@bot.message_handler(commands=["start", "help"])
def send_welcome(m):
	name = m.from_user.first_name
	if hasattr(m.from_user, 'last_name') and m.from_user.last_name is not None:
		name += u" {}".format(m.from_user.last_name)

	if hasattr(m.from_user, 'username') and m.from_user.username is not None:
		name += u" @{}".format(m.from_user.username)
	if m.text == "/start":
		bot.send_message(m.chat.id,text_messages['welcome'].format(name=name), reply_markup=inlineForWali())
	else:
		bot.send_message(m.chat.id,text_messages['info'], parse_mode="Markdown", reply_markup=inlineForWali())

@bot.message_handler(commands=['bantu'])
def bantuan(m):
	bot.send_message(m.chat.id,text_messages['info'])

def telegram_polling():
	try:
		bot.polling(none_stop=True)
	except Exception:
		bot.stop_polling()
		time.sleep(5)
		telegram_polling()

if __name__ == '__main__':
	telegram_polling()