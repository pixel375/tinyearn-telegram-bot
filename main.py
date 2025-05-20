from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio

BOT_TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)
bot_app = Application.builder().token(BOT_TOKEN).build()

# Register command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to TinyEarn!\nUse /shorten <url> or /ref to get started.")

async def ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your referral link:\nhttps://tinyearn.com/?ref={user_id}")

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("ref", ref))

# Async init wrapper for Flask route
async def handle_update(data):
    await bot_app.initialize()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    asyncio.run(handle_update(data))
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
