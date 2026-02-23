
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ====== НАСТРОЙКИ ======
BOT_TOKEN = "8218142823:AAFlWcFYx8RQ_k7BDy90VcVzTyhRXh36als"
ADMIN_USERNAME = "@charmparadox"  # Username администратора
# =======================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Текст прайса
PRICE_TEXT = (
    "💰 <b>Прайс-лист:</b>\n\n"
    "1) Обработка\n"
    "   — 10 рублей\n\n"
    "2) Пикча\n"
    "   — 10 рублей — один персонаж\n"
    "   — 15 рублей — два персонажа\n"
    "   — 20 рублей — три и более персонажей\n\n"
    "3) Видео\n"
    "   — 20 рублей"
)

# Главная клавиатура
def get_keyboard():
    keyboard = [
        [KeyboardButton("💰 Прайс"), KeyboardButton("👤 Администратор")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выбери нужный раздел 👇",
        reply_markup=get_keyboard()
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💰 Прайс":
        await update.message.reply_html(PRICE_TEXT)

    elif text == "👤 Администратор":
        await update.message.reply_text(
            f"Связаться с администратором: {ADMIN_USERNAME}"
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()


