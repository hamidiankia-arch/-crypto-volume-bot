import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID
from crypto_analyzer import CryptoAnalyzer

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class CryptoVolumeBot:
    def __init__(self):
        self.analyzer = CryptoAnalyzer()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور /start"""
        welcome_text = """
        🤖 **ربات تحلیل حجم معاملات ارزهای دیجیتال**
        
        برای دریافت لیست ارزهایی که حجم معاملات امروزشان از مجموع 3 روز گذشته بیشتر است، از دستور زیر استفاده کنید:
        
        /volume
        
        🎯 **شرط فیلتر:** 
        حجم امروز > مجموع حجم 3 روز گذشته
        
        📊 **داده‌ها از:** CoinGecko API
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def volume_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور /volume برای دریافت ارزهای واجد شرط"""
        await update.message.reply_text("🔄 در حال آنالیز داده‌های بازار... لطفاً منتظر بمانید.")
        
        try:
            qualified_coins = self.analyzer.analyze_volume_condition()
            
            if not qualified_coins:
                await update.message.reply_text("❌ هیچ ارزی با این شرط یافت نشد.")
                return
            
            # ساخت پیام نتیجه
            result_text = "🎯 **ارزهای با حجم امروز بیشتر از مجموع 3 روز گذشته:**\n\n"
            
            for i, coin in enumerate(qualified_coins, 1):
                increase_percent = (coin['volume_increase_ratio'] - 1