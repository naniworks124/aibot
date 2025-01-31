import requests
from telebot import TeleBot

# Telegram Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = TeleBot(BOT_TOKEN)

# Gemini API Key
API_KEY = "YOUR_GEMINI_API_KEY"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

# Define the '/start' command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I am your assistant bot. Ask me anything.")

# Define the message handler for normal text messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Send typing action to Telegram
    bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # Get the message text
    ms = message.text

    # Prepare the API request payload for Gemini API
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
        bot.reply_to(message, error_message, parse_mode="HTML")

# Start the bot
bot.polling()
