import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Отправь /calc <цена_покупки> <прибыль>")

@bot.message_handler(commands=['calc'])
def calc(message):
    try:
        args = message.text.split()[1:]
        if len(args) != 2:
            bot.send_message(message.chat.id, "Формат: /calc 3.72 0.10 (цена и прибыль)")
            return

        price = float(args[0])
        profit = float(args[1])
        commission = 0.001

        sell_price = price * (1 + profit) / (1 - commission)
        sell_price = round(sell_price, 4)

        bot.send_message(message.chat.id, f"Минимальная цена продажи: {sell_price} PLN")

    except:
        bot.send_message(message.chat.id, "Ошибка. Пример: /calc 3.72 0.10")

bot.polling()
