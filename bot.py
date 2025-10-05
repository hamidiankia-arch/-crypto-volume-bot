import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN
from crypto_analyzer import CryptoAnalyzer

logging.basicConfig(level=logging.INFO)

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    async def start(update, context):
        await update.message.reply_text("🤖 Crypto Volume Bot - /volume")
    
    async def volume(update, context):
        await update.message.reply_text("📊 Analyzing market data...")
        try:
            analyzer = CryptoAnalyzer()
            coins = analyzer.analyze_volume_condition()
            
            if coins:
                response = "✅ Qualified coins found!"
            else:
                response = "❌ No coins match the condition"
                
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text("❌ Error analyzing data")
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("volume", volume))
    
    print("🤖 Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()