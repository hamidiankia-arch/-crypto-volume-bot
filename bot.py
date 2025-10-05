import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN
from crypto_analyzer import CryptoAnalyzer

logging.basicConfig(level=logging.INFO)

class CryptoVolumeBot:
    def __init__(self):
        self.analyzer = CryptoAnalyzer()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🤖 ربات تحلیل حجم ارزهای دیجیتال - /volume")
    
    async def volume_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔄 در حال آنالیز...")
        
        try:
            coins = self.analyzer.analyze_volume_condition()
            
            if not coins:
                await update.message.reply_text("❌ هیچ ارزی یافت نشد.")
                return
            
            result_text = "🎯 ارزهای واجد شرط:\n\n"
            for i, coin in enumerate(coins, 1):
                result_text += f"{i}. {coin['name']} ({coin['symbol']})\n"
            
            await update.message.reply_text(result_text)
                
        except Exception as e:
            await update.message.reply_text("❌ خطا در دریافت داده‌ها")

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده")
    
    app = Application.builder().token(BOT_TOKEN).build()
    bot = CryptoVolumeBot()
    
    app.add_handler(CommandHandler("start", bot.start_command))
    app.add_handler(CommandHandler("volume", bot.volume_command))
    
    print("🤖 ربات فعال شد...")
    app.run_polling()

if __name__ == '__main__':
    main()