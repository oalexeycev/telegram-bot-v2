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
@app.post(f"/{TOKEN}")
async def webhook(request: Request):
    print("Telegram прислал запрос!")  # ← добавь это
    body = await request.json()
    print("Body:", body)  # ← и это
    update = Update.de_json(body, telegram_app.bot)
    if update:
        print("Update:", update.to_dict())  # ← и это
        await telegram_app.process_update(update)
    return {"ok": True}