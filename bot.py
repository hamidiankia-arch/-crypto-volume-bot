cat > simple_bot.py << 'EOF'
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8399544330:AAGwga10CEep0mUMDdiZRn44V5JcWYLERhA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من فعال شدم ✅")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تست موفق ✅")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    print("ربات اجرا شد...")
    app.run_polling()

if __name__ == '__main__':
    main()
EOF

python simple_bot.py