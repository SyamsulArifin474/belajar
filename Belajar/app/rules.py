from telebot import types

def inlineForWali():
	markup = types.InlineKeyboardMarkup()
	markup.row(
		types.InlineKeyboardButton("Absensi", callback_data="bantu"),
		types.InlineKeyboardButton("Bantuan", callback_data="bantu")
	)
	markup.row(
		types.InlineKeyboardButton("Hubungi Kami", url="t.me/MoujieboulChoire"),
	)
	return markup
		# return markup