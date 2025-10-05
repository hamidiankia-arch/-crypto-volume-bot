import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    async def start(update, context):
        await update.message.reply_text("🤖 ربات فعال شد! از /volume استفاده کنید")
    
    async def volume(update, context):
        await update.message.reply_text("📊 تحلیل حجم در حال توسعه... به زودی")
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("volume", volume))
    
    print("🤖 ربات فعال شد...")
    app.run_polling()

if __name__ == '__main__':
    main()