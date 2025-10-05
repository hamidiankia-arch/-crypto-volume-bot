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
                increase_percent = (coin['volume_increase_ratio'] - 1) * 100
                result_text += f"{i}. **{coin['name']}** ({coin['symbol']})\n"
                result_text += f"   💰 قیمت: ${coin['current_price']:,.2f}\n"
                result_text += f"   📈 افزایش حجم: {increase_percent:+.1f}%\n"
                result_text += f"   🏦 مارکت‌کپ: ${coin['market_cap']:,.0f}\n"
                result_text += f"   🔥 حجم امروز: ${coin['today_volume']:,.0f}\n"
                result_text += f"   📊 حجم ۳ روز گذشته: ${coin['last_3_days_volume']:,.0f}\n\n"
            
            # اضافه کردن تاریخ به پیام
            from datetime import datetime
            result_text += f"🕒 آخرین بروزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # ارسال پیام (تقسیم در صورت طولانی بودن)
            if len(result_text) > 4096:
                # تقسیم پیام به بخش‌های کوچکتر
                for x in range(0, len(result_text), 4096):
                    await update.message.reply_text(
                        result_text[x:x+4096], 
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
            else:
                await update.message.reply_text(
                    result_text, 
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
                
        except Exception as e:
            logging.error(f"Error in volume command: {e}")
            await update.message.reply_text("❌ خطایی در دریافت داده‌ها رخ داد. لطفاً بعداً تلاش کنید.")

def main():
    """تابع اصلی برای اجرای ربات"""
    if not BOT_TOKEN:
        raise ValueError("لطفاً BOT_TOKEN را در فایل .env تنظیم کنید")
    
    # ایجاد اپلیکیشن
    application = Application.builder().token(BOT_TOKEN).build()
    bot = CryptoVolumeBot()
    
    # ثبت هندلرها
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("volume", bot.volume_command))
    
    # اجرای ربات
    print("🤖 ربات فعال شد...")
    application.run_polling()

if __name__ == '__main__':
    main()