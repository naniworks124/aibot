import os
import requests
from telebot import TeleBot

# Get the bot token and API key from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

if not BOT_TOKEN or not API_KEY:
    raise ValueError("Both BOT_TOKEN and API_KEY must be set as environment variables")

# Initialize the bot with the token
bot = TeleBot(BOT_TOKEN)

# Send typing action
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # Get the message text
    ms = message.text

    # Gemini API URL
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

    # Prepare API request payload
    payload = {
        "contents": [
            {"parts": [{"text": ms}]}
        ]
    }

    try:
        # Fetch the data from Gemini API directly
        response = requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()  # Raise error if request fails

        # Extract the response message from Gemini API
        data = response.json()
        msg = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "❌ Error: No response from Gemini.")

        # Send the response back to Telegram
        bot.send_message(chat_id=message.chat.id, text=msg, parse_mode="Markdown", reply_to_message_id=message.message_id)

    except Exception as e:
        # Handle errors
        error_message = "<b>❌ Error Occurred! Please Contact @NitinJack</b>\n"
        bot.reply_text(chat_id=message.chat.id, reply_to_message_id=message.message_id, text=error_message, parse_mode="HTML")


# Start the bot
if __name__ == "__main__":
    bot.polling(none_stop=True)
