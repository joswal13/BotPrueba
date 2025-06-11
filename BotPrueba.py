import os
from flask import Flask, request
import telebot

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Asegúrate que esta variable está en Render
print(f"Token leído: {TOKEN!r}")  # Imprime el token entre comillas para detectar espacios o None

if TOKEN is None:
    print("❌ ERROR: La variable de entorno TELEGRAM_TOKEN no está definida.")
    exit(1)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    print(f"✅ Recibido /start de {message.from_user.id}")
    bot.reply_to(message, 
                 """
    hola Soy 🤖MINETBOT, Tu asistente virtual 24/7. 
    
MINET es tu Proveeedor de servicios de internet que te brinda tecnología en Fibra Óptica.
  
Nos enfocados en brindarte el mejor servicio. ¿En que podemos ayudarte ?
   
            \n /start - 💬 Comenzar un nuevo chat
            \n /1 - 👨‍🔧​ Soporte técnico / Problemas con el WiFi
            \n /2 - ​💯 Planes de Servicio de Internet
            \n /3 - 📲 Cambiar contraseña del WiFi ​
            
    """,
                 )
    
@bot.message_handler(commands=["1"])

def send_welcome(message):
    
    bot.reply_to(
        message,
         """
        Soporte técnico / Problemas con el WiFi

        📱 1. Verifica si hay señal en otros dispositivos
            Intenta conectarte desde otro celular, computadora o tablet.Si ningún dispositivo se conecta, probablemente el problema está en tu red, no en el dispositivo.

        ⚠️ 2. Revisa las luces del módem/router
            Luz "LOS" (en rojo o parpadeando): significa pérdida de señal de fibra. Es señal clara de que no hay internet. Luz "Internet" apagada o roja: no hay conexión a internet. Luz "Power" apagada: el módem está apagado o sin energía.

        🔌 3. Reinicia el módem/router
            Apaga el equipo, espera 10-15 segundos y vuelve a encenderlo.Espera 2-3 minutos para que se reinicie completamente.

        🧪 4. Prueba con un cable Ethernet (si tienes uno)
            Conecta directamente tu PC al módem por cable. Si tampoco hay conexión, el problema no es del WiFi, sino del servicio en sí.


        📞 6. Contacta a tu proveedor
            Si después de todo sigue sin funcionar: Llama al soporte técnico (3213819255). Ten a mano nombre y numero de cedula del titular y revisa los indicadores del módem antes de llamar (ellos lo pedirán).

        """,
   
    )

@bot.message_handler(commands=["2"])

def send_welcome(message):
    
    bot.reply_to(
        message,
         """
        Planes de Servicio de Internet

        1. ⚡ Plan Básico - 100MB x $75000
        2. 🔥 Plan         - 150MB x $85000
        3. 🤩​ Plan        - 200MB x $95000

        """,
   
    )

@bot.message_handler(commands=["3"])

def send_welcome(message):
    
    bot.reply_to(
        message,
         """
        Cambiar contraseña del WiFi:   

        """,
   
    )

def hola(message):
    if message.text.lower() in ["hola", "hello", "hi", ]:
        bot.send_message(
            message.chat.id,
            f""" Hola {message.from_user.first_name}, ¿en qué te puedo ayudar?, elige la opcion del siguiente menu que desees:
   
            \n /start - Comenzar un nuevo chat
            \n /1 - Soporte técnico / Problemas con el WiFi
            \n /2 - Planes de Servicio de Internet
            \n /3 - Cambiar contraseña del WiFi
            
            """
            
        )
    else:
        bot.send_message(
            message.chat.id,
            "Comando no encontrado. Por favor, usa /start para revisar los comandos disponibles",
        )  

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        json_str = request.get_data().decode("utf-8")
        print(f"🚨🚨🚨 Payload recibido:\n{json_str}")
        update = telebot.types.Update.de_json(json_str)

        if update.message:
            chat_id = update.message.chat.id
            text = update.message.text
            print(f"➡️ Mensaje recibido: {text} de {chat_id}")

            if text and text.startswith("/start"):
                bot.send_message(chat_id, "Hola, soy tu bot!")
            elif text and text.startswith("/help"):
                bot.send_message(chat_id, "Puedo ayudarte con /start y /help.")

        return "OK", 200
    except Exception as e:
        print(f"❌ Error procesando update: {e}")
        return "Error", 500


@app.route("/", methods=["GET"])
def home():
    return "Bot online"

if __name__ == "__main__":
    # Obtiene el hostname de Render o usa uno fijo
    hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "botprueba-m9ta.onrender.com")
    WEBHOOK_URL = f"https://{hostname}/{TOKEN}"

    # Configura el webhook de Telegram
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook configurado en: {WEBHOOK_URL}")

    # Inicia el servidor Flask
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Iniciando servidor en puerto {port}")
    app.run(host="0.0.0.0", port=port)
