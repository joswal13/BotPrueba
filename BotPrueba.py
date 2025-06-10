import os
from flask import Flask, request
import telebot
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
if TOKEN is None:
    print("❌ ERROR: La variable de entorno TELEGRAM_TOKEN no está definida.")
    exit(1)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    print(f"✅ Recibido /{message.text[1:]} de {message.from_user.id}")
    if message.text == "/start":
        bot.reply_to(message, "Hola, soy tu bot!")
    elif message.text == "/help":
        bot.reply_to(message, "Puedo ayudarte con /start y /help.")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    start_time = time.time()
    try:
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])  # Procesa con telebot handlers
        elapsed = time.time() - start_time
        print(f"⏱ Procesado en {elapsed:.3f}s")
        return "OK", 200
    except Exception as e:
        print(f"❌ Error procesando update: {e}")
        return "Error", 500

@app.route("/", methods=["GET"])
def home():
    return "Bot online"

if __name__ == "__main__":
    hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "minetbot.onrender.com")
    WEBHOOK_URL = f"https://{hostname}/{TOKEN}"

    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook configurado en: {WEBHOOK_URL}")

    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Iniciando servidor en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=False)  # debug=False para producción
