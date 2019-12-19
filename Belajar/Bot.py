import telebot, time, os
from telebot import types
from app.rules import inlineForWali
from config import conf, text_messages
import flask
from app import views

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

# ini bisa dipanggil kalau ngetik /absensi di bot
@bot.message_handler(commands=['absensi'])
# ini fungsi untuk absensi
def absensi(m):
	bot.send_message(m.chat.id, views.absensi())

# Fungsi untuk callback yang ada di app/rules.py
@bot.callback_query_handler(func=lambda call: True)
def callbackQuery(c):
	try:
		# sesuaikan dengan pengaturan yang ada di app/rules.py callback_data
		# contoh admin_bantu
		if c.data == "admin_bantu":
			bantuan(c.message)
		elif c.data == "admin_absensi":
			absensi(c.message)
	except Exception as e:
		print(e)

def telegram_polling():
	try:
		bot.polling(none_stop=True)
	except Exception:
		bot.stop_polling()
		time.sleep(5)
		telegram_polling()

if __name__ == '__main__':
	telegram_polling()