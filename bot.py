#!/usr/bin/env python3
import os
import json
import random
import logging
from typing import List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# Import configuration
from config import BOT_TOKEN, ADMINS, TRUTHS_FILE, DARES_FILE, DEFAULT_TRUTHS, DEFAULT_DARES

# Logging setup
# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
# File helper functions
def ensure_file(path: str, default_list):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_list, f, ensure_ascii=False, indent=2)

def load_list(path: str) -> List[str]:
    ensure_file(path, [])
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception as e:
        logger.warning(f"Corrupt JSON in {path}: {e}")
    return []

def save_list(path: str, items: List[str]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

# Initialize files
ensure_file(TRUTHS_FILE, DEFAULT_TRUTHS)
ensure_file(DARES_FILE, DEFAULT_DARES)

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Truth", callback_data="truth")],
        [InlineKeyboardButton("Dare", callback_data="dare")],
        [InlineKeyboardButton("Random", callback_data="random")],
    ]
    await update.message.reply_text("Welcome to Truth & Dare! Choose:", reply_markup=InlineKeyboardMarkup(keyboard))

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Your Telegram user id is: {user.id}")

async def get_random_truth():
    truths = load_list(TRUTHS_FILE)
    return random.choice(truths) if truths else "No truths available."

async def get_random_dare():
    dares = load_list(DARES_FILE)
    return random.choice(dares) if dares else "No dares available."

async def truth_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🟣 Truth: {await get_random_truth()}")

async def dare_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔴 Dare: {await get_random_dare()}")

async def random_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.choice([True, False]):
        await update.message.reply_text(f"🟣 Truth: {await get_random_truth()}")
    else:
        await update.message.reply_text(f"🔴 Dare: {await get_random_dare()}")

# Callback for inline buttons
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "truth":
        await query.edit_message_text(f"🟣 Truth: {await get_random_truth()}")
    elif data == "dare":
        await query.edit_message_text(f"🔴 Dare: {await get_random_dare()}")
    elif data == "random":
        if random.choice([True, False]):
            await query.edit_message_text(f"🟣 Truth: {await get_random_truth()}")
        else:
            await query.edit_message_text(f"🔴 Dare: {await get_random_dare()}")

# Admin-only decorator
def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if user and user.id in ADMINS:
            return await func(update, context)
        msg = "❌ You are not authorized to use this command."
        await update.message.reply_text(msg)
    return wrapper
    # Admin commands
@admin_only
async def addtruth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Usage: /addtruth <truth text>")
        return
    truths = load_list(TRUTHS_FILE)
    truths.append(text)
    save_list(TRUTHS_FILE, truths)
    await update.message.reply_text("✅ Truth added successfully!")

@admin_only
async def adddare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Usage: /adddare <dare text>")
        return
    dares = load_list(DARES_FILE)
    dares.append(text)
    save_list(DARES_FILE, dares)
    await update.message.reply_text("✅ Dare added successfully!")

# Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("truth", truth_cmd))
    app.add_handler(CommandHandler("dare", dare_cmd))
    app.add_handler(CommandHandler("random", random_cmd))
    app.add_handler(CommandHandler("addtruth", addtruth))
    app.add_handler(CommandHandler("adddare", adddare))
    app.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("🤖 Bot started successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()
