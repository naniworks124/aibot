import os
import requests
import re
from telebot import TeleBot

# Get the bot token and API key from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

if not BOT_TOKEN or not API_KEY:
    raise ValueError("Both BOT_TOKEN and API_KEY must be set as environment variables")

# Initialize the bot
bot = TeleBot(BOT_TOKEN)

def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")
    ms = message.text

    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": ms}]}
        ]
    }

    try:
        response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()

        data = response.json()
        msg = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "❌ Error: No response from Gemini.")

        msg = escape_markdown(msg)  # Escape markdown before sending
        bot.send_message(chat_id=message.chat.id, text=msg, parse_mode="MarkdownV2", reply_to_message_id=message.message_id)

    except Exception as e:
        error_message = "<b>❌ Error Occurred! Please Contact @NitinJack</b>\n"
        bot.send_message(chat_id=message.chat.id, text=error_message, parse_mode="HTML", reply_to_message_id=message.message_id)

if __name__ == "__main__":
    bot.polling(none_stop=True)
