import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ==============================
# НАСТРОЙКИ — ИЗМЕНИ ЭТО
# ==============================
BOT_TOKEN = "8218142823:AAFlWcFYx8RQ_k7BDy90VcVzTyhRXh36als"
ADMIN_USERNAME = "@charmparadox"  # или номер телефона
ADMIN_CHAT_ID = 8486986323  # необязательно, но можно указать chat_id администратора

# Прайс-лист (измени под себя)
PRICE_TEXT = """
💰 *Прайс-лист*

▪️ Услуга 1 — 50 ₽
▪️ Услуга 2 — 100 ₽
▪️ Услуга 3 — 200 ₽
▪️ Услуга 4 — 300 ₽

_Цены могут меняться. Уточняйте у администратора._
"""
# ==============================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Главное меню — кнопки внизу
MAIN_MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("💰 Прайс"), KeyboardButton("📅 Запись"), KeyboardButton("👤 Администратор")],
    ],
    resize_keyboard=True,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text(
        "👋 Привет! Я ваш помощник.\n\n"
        "Выберите нужный раздел в меню ниже 👇",
        reply_markup=MAIN_MENU,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий кнопок меню и текстовых сообщений"""
    text = update.message.text

    if text == "💰 Прайс":
        await update.message.reply_text(PRICE_TEXT, parse_mode="Markdown")

    elif text == "📅 Запись":
        # Сохраняем состояние — ждём имя
        context.user_data["awaiting_booking"] = True
        await update.message.reply_text(
            "📅 *Запись*\n\n"
            "Напишите ваше имя и удобное время для записи.\n"
            "Например: _Анна, вторник 14:00_",
            parse_mode="Markdown",
        )

    elif text == "👤 Администратор":
        await update.message.reply_text(
            f"👤 *Администратор*\n\n"
            f"Вы можете связаться с нами напрямую:\n"
            f"Telegram: {ADMIN_USERNAME}\n\n"
            f"Или напишите ваш вопрос прямо здесь, и мы передадим его администратору.",
            parse_mode="Markdown",
        )
        context.user_data["awaiting_question"] = True

    elif context.user_data.get("awaiting_booking"):
        # Принимаем заявку на запись
        context.user_data["awaiting_booking"] = False
        user = update.effective_user
        logger.info(f"Новая запись от {user.full_name} (@{user.username}): {text}")

        await update.message.reply_text(
            "✅ Ваша заявка принята!\n\n"
            f"Данные: _{text}_\n\n"
            "Мы свяжемся с вами для подтверждения.",
            parse_mode="Markdown",
            reply_markup=MAIN_MENU,
        )

        # Уведомление администратору (если указан ADMIN_CHAT_ID)
        if ADMIN_CHAT_ID:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"📅 Новая запись!\n"
                     f"От: {user.full_name} (@{user.username})\n"
                     f"Данные: {text}",
            )

    elif context.user_data.get("awaiting_question"):
        # Принимаем вопрос для администратора
        context.user_data["awaiting_question"] = False
        user = update.effective_user
        logger.info(f"Вопрос от {user.full_name} (@{user.username}): {text}")

        await update.message.reply_text(
            "✅ Ваш вопрос отправлен администратору!\n"
            "Мы ответим вам в ближайшее время.",
            reply_markup=MAIN_MENU,
        )

        if ADMIN_CHAT_ID:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"❓ Вопрос администратору!\n"
                     f"От: {user.full_name} (@{user.username})\n"
                     f"Вопрос: {text}",
            )

    else:
        # Любое другое сообщение
        await update.message.reply_text(
            "Используйте кнопки меню ниже 👇",
            reply_markup=MAIN_MENU,
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()

