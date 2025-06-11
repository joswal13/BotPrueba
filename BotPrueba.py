import os
from flask import Flask, request
import telebot

# Leer token desde variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")
print(f"Token leído: {TOKEN!r}")

if not TOKEN:
    print("❌ ERROR: La variable de entorno TELEGRAM_TOKEN no está definida.")
    exit(1)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ============================
# HANDLERS de comandos Telegram
# ============================

@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    bot.reply_to(message, """
Hola Soy 🤖MINETBOT, Tu asistente virtual 24/7. 

MINET es tu proveedor de servicios de internet con tecnología en Fibra Óptica.

¿En qué podemos ayudarte?

    /start - 💬 Comenzar un nuevo chat
    /1 - 👨‍🔧 Soporte técnico / Problemas con el WiFi
    /2 - 💯 Planes de Servicio de Internet
    /3 - 📲 Cambiar contraseña del WiFi
""")

@bot.message_handler(commands=["1"])
def handle_support(message):
    bot.reply_to(message, """
Soporte técnico / Problemas con el WiFi

📱 Verifica si hay señal en otros dispositivos  
⚠️ Revisa las luces del módem/router  
🔌 Reinicia el módem/router  
🧪 Prueba con un cable Ethernet  
📞 Contacta a soporte técnico: 3213819255  
""")

@bot.message_handler(commands=["2"])
def handle_plans(message):
    bot.reply_to(message, """
Planes de Servicio de Internet:

1. ⚡ Básico - 100MB x $75.000  
2. 🔥 Medio - 150MB x $85.000  
3. 🤩 Avanzado - 200MB x $95.000
""")

@bot.message_handler(commands=["3"])
def handle_wifi_change(message):
    bot.reply_to(message, """
Para cambiar la contraseña del WiFi, ingresa al panel de administración de tu router desde tu navegador con la dirección 192.168.1.1 o 192.168.0.1.  
Usuario: admin  
Contraseña: admin o la que tengas configurada.
""")

# ============================
# Webhook para recibir mensajes
# ============================
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])  # Usa handlers definidos arriba
        return "OK", 200
    except Exception as e:
        print(f"❌ Error procesando update: {e}")
        return "Error", 500

# ============================
# Ruta raíz
# ============================
@app.route("/", methods=["GET"])
def home():
    return "Bot online ✅"

# ============================
# Ruta manual para configurar el webhook
# ============================
@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "botprueba-m9ta.onrender.com")
    webhook_url = f"https://{hostname}/{TOKEN}"
    bot.remove_webhook()
    success = bot.set_webhook(url=webhook_url)
    print(f"🔧 Webhook configurado manualmente: {webhook_url}")
    return f"Webhook set: {success}, URL: {webhook_url}"

# ============================
# Arranque local (no usado en Render)
# ============================
if __name__ == "__main__":
    hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "botprueba-m9ta.onrender.com")
    WEBHOOK_URL = f"https://{hostname}/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook configurado en: {WEBHOOK_URL}")
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Iniciando servidor Flask en puerto {port}")
    app.run(host="0.0.0.0", port=port)
