import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "TON_TOKEN_ICI")  # Remplace si besoin
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://tonapp.onrender.com/webhook")  # Change après déploiement

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()


# --- Commandes du bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bienvenue sur Business Chine !\nTape /help pour commencer.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 Commandes disponibles :\n/start - Démarrer\n/help - Aide")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Vous avez dit : {update.message.text}")


# --- Handlers ---
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# --- Webhook Flask ---
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK", 200


# --- Point de test ---
@app.route('/')
def home():
    return "Bot en ligne ✅", 200


if name == '__main__':
    # Démarre le serveur Flask
    port = int(os.environ.get("PORT", 5000))
    print(f"✅ Serveur en ligne sur le port {port}")

    # Configure le webhook
    import asyncio
    from telegram import Bot

    async def set_webhook():
        bot = Bot(token=TOKEN)
        await bot.delete_webhook()
        await bot.set_webhook(url=WEBHOOK_URL)

    asyncio.run(set_webhook())

    app.run(host='0.0.0.0', port=port)
