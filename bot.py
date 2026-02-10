import os
import logging
import telegram

print("telegram package:", telegram.__file__)
print("telegram version:", telegram.__version__)

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "🎲 Este grupo es para organizar partidas, hablar de juegos de mesa y pasarlo bien.\n\n"
    "━━━━━━━━━━━━\n"
    "NORMAS BÁSICAS\n"
    "━━━━━━━━━━━━\n"
    "• Respeto ante todo: no se toleran insultos ni ataques hacia personas o colectivos.\n"
    "• Nada de spam, contenido +18 ni temas ajenos a la asociación\n"
    "• No publiques información privada o confidencial\n"
    "• Si hay un problema → contacta con moderación\n\n"
    "━━━━━━━━━━━━\n"
    "USO DE CANALES\n"
    "━━━━━━━━━━━━\n"
    "📢 Eventos → solo publica la organización\n"
    "🗓 Próximas partidas → publicación reservada a socios\n"
    "💰 Compra/Venta → solo anuncios\n"
    "📷 Fotos → solo fotos\n\n"
    "En estos canales:\n"
    "👉 no responder ni debatir\n"
    "👉 usar reacciones\n"
    "👉 contactar por privado si te interesa algo\n\n"
    "¡Ahora sí… a jugar! 🎲"
)

# comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Hola mundo 👋")

# bienvenida automática
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not update.message or not update.message.new_chat_members:
        return

    # Si entran varios a la vez, manda 1 solo mensaje
    nombres = [u.first_name for u in update.message.new_chat_members]
    lista = ", ".join(nombres)
    
    logger.info(
        "Mensaje de bienvenida para: %s", lista
    )
    
    await msg.reply_text(
        f"👋 ¡Bienvenid@s {lista}!\n\n" + WELCOME_TEXT
    )

# comando /prueba -> simula bienvenida
async def prueba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    logger.info(
        "prueba de %s",nombre
    )
    await update.effective_message.reply_text(
        f"👋 ¡Hola {nombre}!\n\n"  # + WELCOME_TEXT
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Exception while handling an update:", exc_info=context.error)
    
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN no está llegando al proceso (Railway Variables).")    

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("prueba", prueba))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

app.add_error_handler(error_handler)

print("Bot funcionando...")
app.run_polling()

