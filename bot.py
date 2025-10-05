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
        welcome_text = """
        🤖 ربات تحلیل حجم معاملات ارزهای دیجیتال
        
        برای دریافت لیست ارزهایی که حجم معاملات امروزشان از مجموع 3 روز گذشته بیشتر است، از دستور زیر استفاده کنید:
        
        /volume
        """
        await update.message.reply_text(welcome_text)
    
    async def volume_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔄 در حال آنالیز داده‌های بازار... لطفاً منتظر بمانید.")
        
        try:
            qualified_coins = self.analyzer.analyze_volume_condition()
            
            if not qualified_coins: