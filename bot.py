import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

def get_crypto_data():
    """داده‌های ساده از API"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except:
        return []

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    async def start(update, context):
        await update.message.reply_text("🤖 ربات تحلیل حجم - /volume")
    
    async def volume(update, context):
        await update.message.reply_text("🔍 در حال بررسی بازار...")
        try:
            coins = get_crypto_data()
            if coins:
                names = [coin['name'] for coin in coins[:5]]
                response = "🏆 5 ارز برتر:\n" + "\n".join(names)
            else:
                response = "❌ خطا در دریافت داده"
                
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text("❌ خطا در تحلیل")
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("volume", volume))
    
    print("🤖 ربات فعال شد...")
    app.run_polling()

if __name__ == '__main__':
    main()