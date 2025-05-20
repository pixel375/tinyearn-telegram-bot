import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ.get("BOT_TOKEN")  # Set your token as an env variable

app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to TinyEarn!")

bot_app.add_handler(CommandHandler("start", start))

# --- Init ---
async def init_bot():
    await bot_app.initialize()
    await bot_app.start()

@app.before_first_request
def before_first_request():
    asyncio.run(init_bot())

# --- Webhook ---
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.run(bot_app.process_update(update))  # Fixed line
    return "ok"

# --- Main ---
if __name__ == "__main__":
    app.run(port=5000)
