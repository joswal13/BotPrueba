import os
from flask import Flask, request
import telebot

# Leer token desde variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")
#print(f"Token leído: {TOKEN!r}")

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
    #print(f"✅ Handler /start invocado desde chat {message.chat.id}")
    bot.reply_to(message, """
Hola Soy 🤖MINETBOT, Tu asistente virtual 24/7. 

MINET es tu proveedor de servicios de internet con tecnología en Fibra Óptica.

Nos enfocados en brindarte el mejor servicio. ¿En qué podemos ayudarte?

    /start - 💬 Comenzar un nuevo chat
    /SoporteTecnico - 👨‍🔧 Soporte técnico / Problemas con el WiFi
    /Planes - 💯 Planes de Servicio de Internet
    /CambioClaveWifi - 📲 Cambiar contraseña del WiFi
""")

@bot.message_handler(commands=["SoporteTecnico"])
def handle_support(message):
    #print(f"✅ Handler /SoporteTecnico invocado desde chat {message.chat.id}")
    bot.reply_to(message, """
Soporte técnico / Problemas con el WiFi

     📱 Verifica si hay señal en otros dispositivos 
        (Intenta conectarte desde otro celular, 
        computadora o tablet.Si ningún dispositivo 
        se conecta, probablemente el problema está 
        en tu red, no en el dispositivo.) 

     ⚠️ Revisa las luces del módem/router :
        *Luz "Power" apagada: el módem está apagado o sin energía.
        Posible Falla con la fuente de poder)
        
        * Luz "PON" o "LOS" en rojo o parpadeando: 
        significa pérdida de señal de fibra. 
        Es señal clara de que no hay internet. 
        
        *Luz "WLA" o "Internet" o "wifi" apagada: 
        no hay conexión a internet.       
        
     🔌 Reinicia el módem/router  (Apaga el equipo, 
        espera 10-15 segundos y vuelve a encenderlo.
        Espera 2-3 minutos para que se reinicie completamente.)
                
     🧪 Prueba con un cable Ethernet  ( Conecta directamente tu PC 
        al módem por cable. Si tampoco hay conexión, 
        el problema no es del WiFi, sino del servicio en sí.)
                
     📞 Contacta a soporte técnico: 3213819255  ( Si después de
        todo sigue sin funcionar: Llama al soporte técnico (3213819255).
        Ten a mano; nombre y numero de cedula del titular y revisa los
        indicadores del módem antes de llamar (ellos lo pedirán).)
""")

@bot.message_handler(commands=["Planes"])
def handle_plans(message):
    #print(f"✅ Handler /Planes invocado desde chat {message.chat.id}")
    bot.reply_to(message, """
Planes de Servicio de Internet:

    1. ⚡ Plan Básico  100 Mbps x $75.000  
                
    2. 🔥 Plan Intermedio  150 Mbps x $85.000  

    3. 🤩 Plan Avanzado  200 Mbps x $95.000

    4. 🤯​ Plan Premium  +200 Mbps 
          Para Solicitar mas megas comunicate con nuestras oficinas al 3213819255
""")

@bot.message_handler(commands=["CambioClaveWifi"])
def handle_wifi_change(message):
    #print(f"✅ Handler /CambioClaveWifi  invocado desde chat {message.chat.id}")
    bot.reply_to(message, """
Para cambiar la contraseña del WiFi, ingresa al panel de administración de tu router desde tu navegador con la dirección 192.168.1.1 o 192.168.0.1.  
Usuario: admin  
Contraseña: admin o la que tengas configurada.
""")

# ✅ Imprimir handlers después de registrarlos
#print(f"📋 Handlers registrados: {bot.message_handlers}")

# ============================
# Webhook para recibir mensajes
# ============================
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    try:
        json_str = request.get_data().decode("utf-8")
        #print(f"🚨🚨🚨 Payload recibido:\n{json_str}")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200
    except Exception as e:
        print(f"❌ Error procesando update: {e}")
        return "Error", 500

@app.route("/", methods=["GET"])
def home():
    return "Bot online ✅"

@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "botprueba-m9ta.onrender.com")
    webhook_url = f"https://{hostname}/{TOKEN}"
    bot.remove_webhook()
    success = bot.set_webhook(url=webhook_url)
    #print(f"🔧 Webhook configurado manualmente: {webhook_url}")
    return f"Webhook set: {success}, URL: {webhook_url}"

# ============================
# Solo para pruebas locales (NO usado por Render)
# ============================
if __name__ != "__main__":
    hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "botprueba-m9ta.onrender.com")
    webhook_url = f"https://{hostname}/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    #print(f"✅ Webhook configurado automáticamente en producción: {webhook_url}")
    port = int(os.environ.get("PORT", 5000))
    #print(f"🚀 Iniciando servidor Flask en puerto {port}")
    app.run(host="0.0.0.0", port=port)
