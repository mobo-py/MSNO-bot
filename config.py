import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# =========================
# Discord
# =========================

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

# =========================
# Channels
# =========================

DAILY_CHANNEL_ID = int(os.getenv("DAILY_CHANNEL_ID"))
GOALS_CHANNEL_ID = int(os.getenv("GOALS_CHANNEL_ID"))

# =========================
# Roles
# =========================

MASTERMIND_ROLE_ID = int(os.getenv("MASTERMIND_ROLE_ID"))

# =========================
# Scheduler
# =========================

CHECKIN_HOUR = int(os.getenv("CHECKIN_HOUR"))
CHECKIN_MINUTE = int(os.getenv("CHECKIN_MINUTE"))

TIMEZONE = os.getenv("TIMEZONE")