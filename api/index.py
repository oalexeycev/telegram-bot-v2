import os
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN not set in .env or env vars")

app = FastAPI()

# Создаём приложение один раз (global)
telegram_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я бот на Vercel с webhook 🚀")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

# Добавляем handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook endpoint — Vercel будет слать POST сюда
@app.post(f"/{TOKEN}")  # путь = /твой_токен (безопасно, Telegram использует токен в URL)
async def webhook(request: Request):
    if request.method == "POST":
        body = await request.json()
        update = Update.de_json(body, telegram_app.bot)
        await telegram_app.process_update(update)
        return Response(status_code=200)
    return Response(status_code=405)

# Для теста: GET на корень — просто чтобы Vercel видел функцию
@app.get("/")
async def root():
    return {"message": "Telegram bot webhook ready"}