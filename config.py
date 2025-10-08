import os

# Load bot token (from Heroku config vars or local .env)
BOT_TOKEN = "8249629342:AAEpKXueDGyMpir91bprbdQ8OtotDKvnys8"

# Admins (Telegram user IDs allowed to add/remove truths/dares)
ADMINS = [5268691896]  # Example: [123456789]

# File names
TRUTHS_FILE = "truths.json"
DARES_FILE = "dares.json"

# Default content
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
