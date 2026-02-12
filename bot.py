import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Простой обработчик команды /start."""
    await update.message.reply_text("Привет! Я минимальный тестовый бот 🙂")


def main() -> None:
    """
    Точка входа в бота.

    Перед запуском нужно установить переменную окружения TELEGRAM_BOT_TOKEN
    со значением токена вашего бота.
    """
    if not TOKEN:
        raise RuntimeError(
            "Не задан TELEGRAM_BOT_TOKEN. "
            "Установите переменную окружения TELEGRAM_BOT_TOKEN и перезапустите бота."
        )

    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Запускаем long polling
    app.run_polling()


if __name__ == "__main__":
    main()

