import logging
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Connexion à la base SQLite
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY, username TEXT)")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    cursor.execute("INSERT OR IGNORE INTO members (id, username) VALUES (?,?)", (user.id, user.username))
    conn.commit()
    welcome_text = (
    f"👋 Bienvenue {user.mention_html()} dans Business Chine - Alibaba & Shein Pro !\n\n"
    f"📘 Télécharge ton guide ici : [Guide PDF](https://example.com/guide.pdf)\n"
    f"📆 Planning : /planning\n❓ FAQ : /faq"
)

async def guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 Voici ton guide PDF : https://example.com/guide.pdf")

async def planning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📆 Prochaine session : Samedi à 20h sur Zoom")

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ FAQ : \n1. Comment trouver un fournisseur fiable ?\n2. Comment éviter les arnaques Alibaba ?")

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📩 Contacte l'admin : @ChinaAdmin")

async def anti_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "http" in update.message.text.lower():
        await update.message.delete()

if __name__ == "__main__":
    app = ApplicationBuilder().token(config.TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("guide", guide))
    app.add_handler(CommandHandler("planning", planning))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), anti_spam))

    print("🤖 Bot démarré...")
    app.run_polling()
