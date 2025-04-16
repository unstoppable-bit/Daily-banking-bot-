
import telebot
import os
import time
import threading
from datetime import datetime, timedelta

# Настройки
TOKEN = "7618554401:AAHcKSfKtGDZKLeyi9AWdi9ldK-AX2DI7Mg"
ADMIN_ID = 573740356
SEND_HOUR = 8
TRIAL_DAYS = 7

bot = telebot.TeleBot(TOKEN)
users = {}  # user_id: start_date

# Пример базы слов
words = [
    {"term": "Leverage", "translation": "Кредитное плечо", "definition": "Using borrowed money to amplify returns.", "example": "Banks use leverage to increase profit."},
    {"term": "Asset", "translation": "Актив", "definition": "Something of value owned by an individual or organization.", "example": "Cash and property are common assets."}
]

# Пример советов
tips = [
    "Use the STAR method: Situation, Task, Action, Result.",
    "Always prepare your own questions for the interviewer.",
    "Review key finance terms before your interview."
]

# Проверка доступа
def has_access(user_id):
    if user_id == ADMIN_ID:
        return True
    if user_id not in users:
        return False
    start = users[user_id]
    return datetime.now() <= start + timedelta(days=TRIAL_DAYS)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    uid = message.chat.id
    if uid not in users:
        users[uid] = datetime.now()
        bot.send_message(uid, "Welcome to Banking Buddy! You now have 7 days of free access.")
    else:
        bot.send_message(uid, "Welcome back!")

    show_menu(uid)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "**Available Commands:**
"
        "/start – Introduction and access
"
        "/help – Show commands
"
        "/word – Get a banking English word
"
        "/tip – Get a finance/career tip
"
        "/subscribe – Info on paid access
"
        "/id – Your Telegram ID"
    )
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['id'])
def send_id(message):
    bot.send_message(message.chat.id, f"Your Telegram ID is: {message.chat.id}")

@bot.message_handler(commands=['subscribe'])
def send_subscribe(message):
    text = (
        "**Banking Buddy Premium**

"
        "Your 7-day free trial includes:
"
        "- Daily banking words with examples
"
        "- Career tips for finance and banking

"
        "To continue using after the trial:
"
        "• Monthly: 19 zł or 4.99 EUR
"
        "• Payment methods: Crypto, Card, Telegram Pay (coming soon)

"
        "We'll send you the payment link soon."
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['word'])
def send_word(message):
    if has_access(message.chat.id):
        for item in words:
            msg = f"**{item['term']}** ({item['translation']})\n{item['definition']}\n_Example:_ {item['example']}"
            bot.send_message(message.chat.id, msg, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Your access has expired. Use /subscribe to renew.")

@bot.message_handler(commands=['tip'])
def send_tip(message):
    if has_access(message.chat.id):
        for tip in tips:
            bot.send_message(message.chat.id, f"**Career Tip:**\n{tip}", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Your access has expired. Use /subscribe to renew.")

def show_menu(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/word", "/tip", "/help", "/subscribe")
    bot.send_message(chat_id, "Use the menu below to navigate:", reply_markup=keyboard)

# Ежедневная авторассылка (только активным)
def daily_sender():
    sent_today = False
    while True:
        now = datetime.now()
        if now.hour == SEND_HOUR and not sent_today:
            word = words[now.day % len(words)]
            tip = tips[now.day % len(tips)]
            for user_id in users:
                if has_access(user_id):
                    try:
                        msg_word = f"**{word['term']}** ({word['translation']})\n{word['definition']}\n_Example:_ {word['example']}"
                        msg_tip = f"**Career Tip:**\n{tip}"
                        bot.send_message(user_id, msg_word, parse_mode='Markdown')
                        bot.send_message(user_id, msg_tip, parse_mode='Markdown')
                    except Exception as e:
                        print(f"Error sending to {user_id}: {e}")
            sent_today = True
        elif now.hour != SEND_HOUR:
            sent_today = False
        time.sleep(60)

# Запуск
threading.Thread(target=daily_sender).start()
bot.infinity_polling()
