import os
import json
import random
import logging
from typing import List

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Files for persistence
TRUTHS_FILE = "truths.json"
DARES_FILE = "dares.json"

# Default content (you can edit these or add via admin commands)
DEFAULT_TRUTHS = [
    "What is your most embarrassing moment?",
    "Have you ever lied to your best friend?",
    "What's a secret you've never told anyone?",
]
DEFAULT_DARES = [
    "Send a funny selfie to this chat.",
    "Do 10 push-ups and send a photo (optional).",
    "Record 15 seconds of you singing the first song that plays in your playlist.",
]

# Admins: list of Telegram user IDs allowed to add/remove items.
# Put your Telegram integer user id(s) here OR use /myid and then edit this file.
ADMINS: List[int] = [5268691896]  # example: [123456789]

# Helper functions for file storage
def ensure_file(path: str, default_list):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_list, f, ensure_ascii=False, indent=2)

def load_list(path: str) -> List[str]:
    ensure_file(path, [])
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
        except Exception as e:
            logger.warning("Corrupt JSON in %s: %s", path, e)
    return []

def save_list(path: str, items: List[str]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

# Initialize files with defaults if empty
ensure_file(TRUTHS_FILE, DEFAULT_TRUTHS)
ensure_file(DARES_FILE, DEFAULT_DARES)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Truth", callback_data="truth")],
        [InlineKeyboardButton("Dare", callback_data="dare")],
        [InlineKeyboardButton("Random", callback_data="random")],
    ]
    reply = "Welcome to Truth & Dare! Choose:"
    await update.message.reply_text(reply, reply_markup=InlineKeyboardMarkup(keyboard))

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Your Telegram user id is: {user.id}")

async def get_random_truth():
    truths = load_list(TRUTHS_FILE)
    if not truths:
        return "No truths available."
    return random.choice(truths)

async def get_random_dare():
    dares = load_list(DARES_FILE)
    if not dares:
        return "No dares available."
    return random.choice(dares)

async def truth_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = await get_random_truth()
    await update.message.reply_text(f"🟣 Truth: {text}")

async def dare_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = await get_random_dare()
    await update.message.reply_text(f"🔴 Dare: {text}")

async def random_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if random.choice([True, False]):
        text = await get_random_truth()
        await update.message.reply_text(f"🟣 Truth: {text}")
    else:
        text = await get_random_dare()
        await update.message.reply_text(f"🔴 Dare: {text}")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "truth":
        text = await get_random_truth()
        await query.edit_message_text(f"🟣 Truth: {text}")
    elif data == "dare":
        text = await get_random_dare()
        await query.edit_message_text(f"🔴 Dare: {text}")
    elif data == "random":
        if random.choice([True, False]):
            text = await get_random_truth()
            await query.edit_message_text(f"🟣 Truth: {text}")
        else:
            text = await get_random_dare()
            await query.edit_message_text(f"🔴 Dare: {text}")

# Admin-only decorator
def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if user and user.id in ADMINS:
            return await func(update, context)
        else:
            msg = "❌ You are not authorized to use this command. Ask an admin to add you."
            if update.message:
                await update.message.reply_text(msg)
            elif update.effective_chat:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    return wrapper

@admin_only
async def addtruth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # usage: /addtruth your truth text...
    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Usage: /addtruth <truth text>")
        return
    truths = load_list(TRUTHS_FILE)
    truths.append
  
