from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)
bot_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to TinyEarn!\nUse /shorten <url> or /ref to get started.")

async def ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your referral link:\nhttps://tinyearn.com/?ref={user_id}")

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("ref", ref))

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.create_task(bot_app.process_update(update))
    return "ok", 200
