import telebot
import requests
import os
from config import BOT_TOKEN, REMOVE_BG_API

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Send me a photo.\nI will remove the background."
    )

@bot.message_handler(content_types=['photo'])
def remove_bg(message):

    bot.reply_to(message,"⏳ Processing image...")

    file_info = bot.get_file(message.photo[-1].file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

    img = requests.get(file_url)

    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": img.content},
        data={"size":"auto"},
        headers={"X-Api-Key": REMOVE_BG_API}
    )

    if response.status_code == requests.codes.ok:

        with open("no_bg.png","wb") as f:
            f.write(response.content)

        bot.send_document(message.chat.id, open("no_bg.png","rb"))

    else:
        bot.reply_to(message,"❌ Error removing background")

bot.infinity_polling()
