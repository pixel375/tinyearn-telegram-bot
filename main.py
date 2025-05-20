from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os
import nest_asyncio

# Apply patch to allow nested event loops (Render needs this)
nest_asyncio.apply()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Flask app
app = Flask(__name__)

# Telegram bot app (uninitialized)
bot_app = Application.builder().token(BOT_TOKEN).build()

# Register handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to TinyEarn!\nUse /shorten <url> or /ref to get started.")

async def ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your referral link:\nhttps://tinyearn.com/?ref={user_id}")

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("ref", ref))

# Initialize the Telegram app once (not on every webhook call)
asyncio.run(bot_app.initialize())

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.create_task(bot_app.process_update(update))  # non-blocking
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
