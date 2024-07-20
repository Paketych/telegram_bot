import telebot
from telebot import types
import random
import requests
import json
from currency_converter import CurrencyConverter


bot = telebot.TeleBot("6883554728:AAEBP5V4iVYdEcHPu2kVqb61YVR_9A0FNXI")

amount = 0

currency = CurrencyConverter()

API = "e209c06ccf735053ecaa9dffc589a172"

poem = ("Очень любят обезьяны \n"
     "Кушать сладкие бананы. \n"
     "Мы на обезьян похожи, \n"
     "И бананы любим тоже.")

@bot.message_handler(commands=["start"])
def start(message):
    photo = open("./hello.jpg", "rb")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Рассказать стихотворение', callback_data='stih')
    btn2 = types.InlineKeyboardButton('фото капибары', callback_data='kap')
    btn3 = types.InlineKeyboardButton('Крутая музыка', callback_data='url')
    markup.row(btn1, btn2)
    markup.row(btn3)
    bot.send_photo(message.chat.id, photo, caption= f'<b>Привет, {message.from_user.first_name}!</b>😎 \n'
                                      f'🔹Это просто бот по имени Виктор Калоедов🥸 \n'
                                      f'🔹Я пока мало что умею, например,  я могу показать вашь id, если вы напишите /id🔢 \n'
                                      f'🔹Также вы можете написать команду /help и вы увидите все, что умеет бот🤖 \n'
                                      f'🔹Еще вы можете вызвать команду /prediction и задать вопрос, тогда я сделаю предсказание🔮 \n'
                                      f'🔹У меня можно узнать погоду в данный момент в любом городе, просто введи команду /weather☀️ \n'
                                      f'🔹С помощью меня вы можете конвертировать валюты, команда /convertation \n'
                                      f'🔹В общем этот бот еще будет развиваться, или же создатель меня просто удалит😀',reply_markup=markup, parse_mode='HTML' )

@bot.message_handler(commands=['pupsik'])
def pupsik(message):
    pupsik = open("./pupsik.mp3", "rb")
    bot.send_audio(message.chat.id, pupsik)

@bot.message_handler(commands=["prediction"])
def prediction(message):
    msg = bot.send_message(message.chat.id, "<b>Задайте закрытый вопрос (на который можно ответить 'да' или 'нет')</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, question)
def question(message):
    listp = ["Без сомнений", 'Да', 'Нет', 'Скорее да', 'Скорее нет', 'Есть сомнения', "Точно да", "Точно нет", 'Духи говорят да', "Духи говорят нет", 'Непонятно']
    prediction = random.choice(listp)
    prove = message.text.lower().find("?")
    if prove != -1:
        bot.send_message(message.chat.id, prediction)
    else:
        bot.send_message(message.chat.id, "Это не вопрос, попробуйте снова:")
        bot.register_next_step_handler(message, question)

@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    markup1 = types.InlineKeyboardMarkup()
    markup2 = types.InlineKeyboardMarkup()
    markup3 = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Удалить фото", callback_data="delete")
    btn2 = types.InlineKeyboardButton("Удалить стихотворение", callback_data="delete")
    btn3 = types.InlineKeyboardButton("Удалить музыку", callback_data="delete")
    markup1.row(btn1)
    markup2.row(btn2)
    markup3.row(btn3)
    photo = open("./kapibara.jpg", "rb")
    url = "https://www.youtube.com/watch?v=7elzoLVEs_w&t=1s"
    if callback.data == 'stih':
        bot.send_message(callback.message.chat.id, poem, reply_markup=markup2)
    elif callback.data == 'kap':
        bot.send_photo(callback.message.chat.id, photo, reply_markup=markup1)
    elif callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'url':
        bot.send_message(callback.message.chat.id, url, reply_markup=markup3)
    elif callback.data == 'RUB/USD':
        values = callback.data.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(callback.message.chat.id, f"💵{amount} {values[0]} = <b>{round(res, 2)}</b> {values[1]}", parse_mode="HTML")
    elif callback.data == 'RUB/EUR':
        values = callback.data.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(callback.message.chat.id, f"💵{amount} {values[0]} = <b>{round(res, 2)}</b> {values[1]}", parse_mode="HTML")
    elif callback.data == 'other':
        bot.send_message(callback.message.chat.id, "❗️<b>Введите валютную пару через знак '/'. (пример: USD/EUR)</b> \n"
                                                   "<b>Валюты:</b> \n"
                                                   "🇺🇸USD - Американский доллар \n"
                                                   "🇪🇺EUR - Евро \n"
                                                   "🇯🇵JPY - Японская Иена\n"
                                                   "🇧🇬BGN - Болгарский лев\n"
                                                   "🇨🇾CYP - Кипрский фунт\n"
                                                   "🇨🇿CZK - Чешская крона\n"
                                                   "🇩🇰DKK - Датская крона\n"
                                                   "🇬🇧GBP - Фунт стерлингов\n"
                                                   "🇨🇦CAD - Канадский доллар\n"
                                                   "🇳🇿NZD - Новозеландский доллар\n"
                                                   "🇨🇳CNY - Китайский юань\n"
                                                   "🇷🇺RUB - Российский рубль\n"
                                                   "🇧🇷BRL - Бразильский реал \n"
                                                   "🇰🇷KRW - Южнокорейская вона \n"
                                                   "🇸🇪SEK - Шведская крона \n"
                                                   "🇹🇷TRY - Турецкая лира", parse_mode="HTML")
        bot.register_next_step_handler(callback.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"💵{amount} {values[0]} = <b>{round(res, 2)}</b> {values[1]}", parse_mode="HTML")
    except Exception:
        bot.send_message(message.chat.id, "Упс😑, что-то пошло не так, впишите валютную пару заново")
        bot.register_next_step_handler(message, my_currency)



@bot.message_handler(commands=["help"])
def main(message):
    bot.send_message(message.chat.id, '<b>Что умеет этот Бот:</b> \n'
                                      '1)🌤Показать погоду в любом городе в данный момент (/weather) \n'
                                      '2)🔮Сделать предсказание на ваш ворос (/prediction) \n'
                                      '3)#️⃣Показать ваш ID в телеграмме (/id) \n'
                                      '4)💵Сконвертировать валютную пару (/convertation) \n'
                                      '4)🔜На этом пока все...', parse_mode='HTML')

@bot.message_handler(commands=["weather"])
def weather(message):
    bot.send_message(message.chat.id, "Введите название города")
    bot.register_next_step_handler(message, get_weather)
def get_weather(message):
    photo = open("./weathergood.png", "rb")
    city = message.text.strip().lower()
    res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API}&units=metric")
    data = json.loads(res.text)
    if data["cod"]=="404":
        bot.send_message(message.chat.id, "❌Такого города нет❌")
    else:
        bot.send_photo(message.chat.id, photo, caption=f"<b>Погода в городе {city}:</b> \n"
                                                       f"🌡<b>Температура:</b> {data["main"]["temp"]} °C \n"
                                                       f"🥵<b>Ощущается как:</b> {data["main"]["feels_like"]} °C \n"
                                                       f"💦<b>Влажность:</b> {data["main"]["humidity"]}% \n"
                                                       f"💨<b>Скорость ветра:</b> {data['wind']["speed"]} м/c", parse_mode='HTML')

@bot.message_handler(commands=['convertation'])
def convert(message):
    bot.send_message(message.chat.id, "Введите сумму для конвертации")
    bot.register_next_step_handler(message, summa)
def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "❌Неверный формат, впишите корректную сумму:")
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("RUB/USD", callback_data="RUB/USD")
        btn2 = types.InlineKeyboardButton("RUB/EUR", callback_data="RUB/EUR")
        btn3 = types.InlineKeyboardButton("Другое значение", callback_data="other")
        markup1.row(btn1, btn2)
        markup1.row(btn3)
        bot.send_message(message.chat.id, "Выберите пару валют", reply_markup=markup1)
    else:
        bot.send_message(message.chat.id, "❌Сумма должна быть больше 0, впишите корректную сумму:")
        bot.register_next_step_handler(message, summa)



@bot.message_handler(commands=['id'])
def ID(message):
    bot.send_message(message.chat.id, f"Ваш id: {message.from_user.id}")


bot.polling(none_stop=True)
