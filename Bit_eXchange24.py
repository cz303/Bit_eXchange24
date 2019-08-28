import telebot
from telebot import TeleBot
from telebot import types
import logging
import time
import requests
import re
from array import array
import random
import string
import json
from emoji import emojize
import schedule

dump = 1
logger = telebot.logger


if dump:
	telebot.logger.setLevel(logging.DEBUG)
#Здесь вводишь API-токен из @botFather.
########################################################
token = "925613654:AAF4NxYjQQe00CMhSDL0g7FEIYxGm_qG9dk"#
########################################################
#Здесь вводишь свой киви.
#####################
qiwi = "+79220175088"#
#####################


bot = telebot.TeleBot(token)
order_number = random.randint(1, 9999)

print('BOT STARTED!')




	
@bot.message_handler(commands=['start'])
def welcome_message(message):
	url = "https://api.cryptonator.com/api/ticker/BTC-RUB"
	req = requests.get(url)
	data = req.json()
	global btc_price
	btc_price = float(data['ticker']['price'])
	print("Курс Bitcoin: ", round(btc_price), " рублей")
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	markup.one_time_keyboard =False
	markup.row('\U0000267B Обменять', '\U000026A0 К прочтению')
	markup.row('\U0001F91D Реф.программа', '\U0001F4F2 Контакты')
	markup.row('\U0001F4E5 Активировать промокод')
	msg = bot.send_message(message.chat.id, "Добро пожаловать в обменник <b>Bit-eX24!</b>",reply_markup=markup, parse_mode= "HTML")
	bot.register_next_step_handler(msg, next)
	
def second_menu(message):
	url = "https://api.cryptonator.com/api/ticker/BTC-RUB"
	req = requests.get(url)
	data = req.json()
	global btc_price
	btc_price = float(data['ticker']['price'])
	print(btc_price)
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	markup.one_time_keyboard =False
	markup.row('\U0000267B Обменять', '\U000026A0 К прочтению')
	markup.row('\U0001F91D Реф.программа', '\U0001F4F2 Контакты')
	markup.row('\U0001F4E5 Активировать промокод')
	msg = bot.send_message(message.chat.id, "Продолжить работу",reply_markup=markup)
	bot.register_next_step_handler(msg, next)

	
def next(message):
	if message.text == '\U0000267B Обменять':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('\U0001F310 Купить BTC', '\U0001F511 Купить Exmo')
		markup.row('\U0001F519 Назад')
		msg = bot.send_message(message.chat.id, " \U00002754 <b>Выберите</b>, что хотите купить:", reply_markup=markup, parse_mode= "HTML")
		bot.register_next_step_handler(msg, buy)
	elif message.text == '\U000026A0 К прочтению':
		bot.send_message(message.chat.id, "\U0001F4A1Важная информация: \n\n\U000025AA Наш бот - @Bit_eX24bot \n\U000025AA При сбое бота - напишите команду - /start \n\U000025AA Транзакция BitCoin отправляется нами максимально возможным приоритетом (1 блок), остальное зависит от самой BTC сети. Ею мы не управляем и никто не управляет \n\U000025AA Не принимаются жалобы на недействующие коды EXMO, если они были переданы третьим лицам или активированы не на сайтах платежных систем соответственно \n\U000025AA Если Вы отправили вместо QIWI на мобильный телефон деньги, то никто вам их не вернет, т.к. мы тоже их не получим. Так же не рассматриваются платежи без комментария \n\U000025AA Всю важную информацию и отзывы мы публикуем в нашем новостном канале - @Bit_eX24 \n\U000025AA On-line поддержка - @Bit_eX24sup, время работы оператора поддержки с 8 утра до 22 вечера \n\U000025AA Бесплатный  прокси при блокировке Telegram https://t.me/proxy?server=142.93.100.244&port=443&secret=086300a794a285f1ceb60fdaecb81cac")
		second_menu(message)
	elif message.text == '\U0001F91D Реф.программа':
		bot.send_message(message.chat.id,"Этот раздел в разработке. <b>Скоро будет.</b>", parse_mode= "HTML")
		second_menu(message)
	elif message.text == '\U0001F4F2 Контакты':
		bot.send_message(message.chat.id,"\U0001F4F2 <b>Контакты:</b> \n\n\U00002709 On-line поддержка - @Bit_ex24sup \n\U0001F52E Новостной канал - t.me/Bit_eX24", parse_mode= "HTML")
		second_menu(message)
	elif message.text == '\U0001F4E5 Активировать промокод':
		msg = bot.send_message(message.chat.id, "\U0001F4DD Введите промокод:")
		bot.register_next_step_handler(msg, promo)
	
def promo(message):
	bot.send_message(message.chat.id, "Промокод <b>не</b> найден!", parse_mode= "HTML")
	second_menu(message)


def buy(message):
	if message.text == '\U0001F310 Купить BTC':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('\U0001F519 Назад')
		msg = bot.send_message(message.chat.id, "Сколько вы хотите купить \U0001F310 <b>BitCoin BTC</b> \n\nНапишите сумму: <b>от 0.0005 до 0.5 BTC</b>", reply_markup=markup, parse_mode= "HTML")
		bot.register_next_step_handler(msg, buy_btc)
	elif message.text == '\U0001F511 Купить Exmo':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('\U0001F519 Назад')
		msg = bot.send_message(message.chat.id, "Сколько вы хотите купить \U0001F511 <b>EXMO-code RUB</b> \n\nНапишите сумму: <b>от 500 до 60000 руб.</b>", reply_markup=markup, parse_mode= "HTML")
		bot.register_next_step_handler(msg, buy_exmo)
	else:
		second_menu(message)
	
def buy_btc(message):
	number = message.text.replace('.','',1).isdigit()
	print(number)
	if message.text == "\U0001F519 Назад":
		second_menu(message)
	elif not number:
		msg = bot.send_message(message.chat.id, "Ошибка! Введите <b>числовое</b> значение:", parse_mode= "HTML")
		bot.register_next_step_handler(msg, buy_btc)
		return
	elif float(message.text) >= 0.51:
		msg = bot.send_message(message.chat.id, "Максимальная сумма обмена: <b>0.5 BTC</b>", parse_mode= "HTML")
		bot.register_next_step_handler(msg, buy_btc)
		return
	elif float(message.text) < 0.0005:
		msg = bot.send_message(message.chat.id, "Минимальная сумма обмена: <b>0.0005 BTC</b>", parse_mode= "HTML")
		bot.register_next_step_handler(msg, buy_btc)
		return
	else:
		global summ 
		summ = float(message.text)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('Согласен','Отмена')
		global total_price
		total_price = float((btc_price * summ)+((btc_price *summ)/8))
		print(total_price)
		msg = bot.send_message(message.chat.id, "\U000026A0 Для получения <b>BitCoin</b> в размере <b>"+str(summ)+" BTC:</b>\n\nВам необходимо оплатить на QiWi кошелек <b>"+str(round(total_price))+" руб.</b>"+"\n\nВы согласны провести обмен?", reply_markup=markup, parse_mode= "HTML")
		bot.register_next_step_handler(msg, ok_button)
	
def buy_exmo(message):
	if message.text == "\U0001F519 Назад":
		second_menu(message)
	elif not message.text.isdigit():
		msg = bot.send_message(message.chat.id, "Ошибка! Введите <b>числовое</b> значение:", parse_mode= "HTML")
		bot.register_next_step_handler(msg, buy_exmo)
		return
	elif float(message.text) < 499:
		msg = bot.send_message(message.chat.id, "Минимальная сумма обмена: <b>500 руб.</b>", parse_mode= "HTML")
		bot.register_next_step_handler(msg, buy_exmo)
		return
	elif float(message.text) > 60000:
		msg = bot.send_message(message.chat.id, "Максимальная сумма обмена: <b>60000 руб.</b>", parse_mode= "HTML")
		bot.register_next_step_handler(msg, buy_exmo)
	else:
		global summ 
		summ = float(message.text)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('Согласен','Отмена')
		global total_price
		total_price = float((summ + (summ/8)))
		msg = bot.send_message(message.chat.id, "\U000026A0 Для получения <b>EXMO</b> в размере "+str(summ)+" руб.\n\nВам необходимо оплатить на QiWi кошелек <b>"+str(round(total_price))+ " руб.</b>\n\nВы согласны провести обмен?", reply_markup=markup, parse_mode= "HTML")
		bot.register_next_step_handler(msg, exmo_pay)
	
	
def ok_button(message):
	if message.text == 'Согласен':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('\U0001F519 Назад')
		msg = bot.send_message(message.chat.id, "\U0001F4DD Пришлите <b>ваш BTC-адрес</b>, на который будут отправлены <b>BitCoin</b>", reply_markup=markup, parse_mode= "HTML")
		bot.register_next_step_handler(msg, bitcoin_kosh)
	else:
		second_menu(message)

def exmo_pay(message):
	if message.text == "Отмена":
		second_menu(message)
	else:
		markup = types.InlineKeyboardMarkup()
		i_pay = types.InlineKeyboardButton('Я оплатил!', callback_data='i_pay_btn')
		cancel = types.InlineKeyboardButton('Отменить заявку', callback_data='cancel_btn')
		markup.add(i_pay, cancel)
		bot.send_message(message.chat.id, "\U00002705 Ваша заявка <b>"HTML""+str(order_number)+"</b> успешно создана. \n\n\U0001F4B3 Переводите на киви кошелёк: \n"+str(qiwi)+" \n\n\U0001F4B0 Сумма к оплате: <b>"+str(round(total_price))+" руб.</b> \n\n\U0000270F Комментарий: <b>"+str(order_number)+"</b> \n\U000026A0 <b>ВАЖНО!</b> Платежи без комментария считаются недействительными! \n\n\U000023F3 <b>Реквизиты действительны:</b> 30 минут. \n\n\U00002757<b>ВНИМАНИЕ</b>\U00002757 После успешного перевода денег по указанным реквизитам нажмите на кнопку Я оплатил, чтобы получить <b>EXMO-код</b>", reply_markup=markup, parse_mode= "HTML")
		second_menu(message)
		return
		schedule.run_pending()
		time.sleep(3000)
		bot.send_message(message.chat.id, "Обмен <b>№2617"+str(order_number)+"</b> отменен по причине <b>отсутствия своевременной оплаты.</b>", parse_mode= "HTML")


def bitcoin_kosh(message):
	if message.text == message.text:
		if re.match('[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', message.text):
			markup = types.InlineKeyboardMarkup()
			i_pay = types.InlineKeyboardButton('Я оплатил!', callback_data='i_pay_btn')
			cancel = types.InlineKeyboardButton('Отменить заявку', callback_data='cancel_btn')
			markup.add(i_pay, cancel)
			bot.send_message(message.chat.id, "\U00002705 Ваша заявка <b>№"+str(order_number)+"</b> успешно создана. \n\n\U0001F4B3 Переводите на киви кошелёк: \n"+str(qiwi)+" \n\n\U0001F4B0 Сумма к оплате: <b>"+str(round(total_price))+" руб.</b> \n\n\U0000270F Комментарий: <b>"+str(order_number)+"</b> \n\U000026A0 <b>ВАЖНО!</b> Платежи без комментария считаются недействительными! \n\n\U000023F3 <b>Реквизиты действительны:</b> 30 минут. \n\n\U00002757<b>ВНИМАНИЕ</b>\U00002757 После успешного перевода денег по указанным реквизитам нажмите на кнопку <b>'Я оплатил'</b>, чтобы получить <b>BTC</b> на ваш адрес", reply_markup=markup, parse_mode= "HTML")
			schedule.run_pending()
			time.sleep(5)
			second_menu(message)
			schedule.run_pending()
			time.sleep(3000)
			bot.send_message(message.chat.id, "Обмен <b>№2617"+str(order_number)+"</b> отменен по причине <b>отсутствия своевременной оплаты.</b>", parse_mode= "HTML")
			second_menu(message)
		else:
			bot.send_message(message.chat.id, "<b>Ошибка!</b> Введите правильный адрес криптокошелька <b>BitСoin</b>", parse_mode= "HTML")
			second_menu(message)
		
		
		
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(call):
	if call.message:
		if call.data == "i_pay_btn":
			bot.answer_callback_query(callback_query_id=call.id, text="\U0000274C Вы ещё не оплатили!", show_alert=True)
		elif call.data == "cancel_btn":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Заявка отменена.")
	
	
if __name__ == '__main__':
	bot.polling(none_stop=True)
