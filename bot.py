import telebot
from flask import Flask, request
import os
import requests

# Load Bot Token from Environment Variables
TOKEN = os.getenv("BOT_TOKEN")  # Set in Koyeb
bot = telebot.TeleBot(TOKEN)

# Flask App for Webhook
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    """Receives Telegram updates via webhook and processes them."""
    update = request.get_data().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

# Function to Escape Markdown Special Characters
def escape_markdown(text):
    """Escapes special characters in Markdown."""
    special_chars = "_*[]()~`>#+-=|{}.!"
    for char in special_chars:
        text = text.replace(char, "\\" + char)
    return text

# Function to Send Query to Gemini API
def ask_gemini(user_text):
    """Sends user message to Gemini API and returns the response."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set this in Koyeb
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText?key={GEMINI_API_KEY}"
    
    payload = {"prompt": user_text, "maxTokens": 100}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers).json()
        return response.get("candidates", [{}])[0].get("output", "Sorry, I couldn't generate a response.")
    
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "❌ AI Error Occurred. Please try again later."

# Function to Handle Messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handles incoming messages from users."""
    try:
        user_text = message.text.strip()
        response = escape_markdown(ask_gemini(user_text))
        bot.send_message(message.chat.id, response, parse_mode="MarkdownV2")

    except telebot.apihelper.ApiTelegramException as e:
        bot.send_message(message.chat.id, "❌ Error Occurred! Please Contact Admin.")
        print(f"Telegram API Error: {e}")

    except Exception as e:
        bot.send_message(message.chat.id, "❌ An unexpected error occurred.")
        print(f"Unexpected Error: {e}")

# Start Flask Web Server
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://your-koyeb-app-url/{TOKEN}")  # Replace with your Koyeb domain
    app.run(host="0.0.0.0", port=8000)
