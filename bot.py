import asyncio

import discord
from discord.ext import commands

import config
from database import create_tables
from scheduler import start_scheduler
from ui.buttons import DailyCheckInView

# --------------------------------------------------
# Intents
# --------------------------------------------------

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

# --------------------------------------------------
# Bot
# --------------------------------------------------

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

persistent_views_added = False
scheduler_started = False

# --------------------------------------------------
# Extensions
# --------------------------------------------------

INITIAL_EXTENSIONS = [
    "cogs.daily_checkin",
    "cogs.weekly_goals",
    "cogs.stats"
]

# --------------------------------------------------
# Ready
# --------------------------------------------------

@bot.event
async def on_ready():

    global persistent_views_added
    global scheduler_started

    print("=" * 50)
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")

    # Register persistent views once
    if not persistent_views_added:
        bot.add_view(DailyCheckInView())
        persistent_views_added = True
        print("✓ Persistent views registered")

    # Sync slash commands ONLY to your server
    try:
        guild = discord.Object(id=config.GUILD_ID)

        bot.tree.copy_global_to(guild=guild)

        synced = await bot.tree.sync(guild=guild)

        print(f"✓ Synced {len(synced)} guild command(s)")

    except Exception as e:
        print("Command Sync Error:")
        print(e)

    # Start scheduler once
    if not scheduler_started:
        await start_scheduler(bot)
        scheduler_started = True
        print("✓ Scheduler started")

    print("✓ Bot Ready")
    print("=" * 50)


# --------------------------------------------------
# Load Cogs
# --------------------------------------------------

async def load_extensions():

    for extension in INITIAL_EXTENSIONS:

        try:
            await bot.load_extension(extension)
            print(f"✓ Loaded {extension}")

        except Exception as e:
            print(f"✗ Failed to load {extension}")
            print(e)


# --------------------------------------------------
# Main
# --------------------------------------------------

async def main():

    await create_tables()

    async with bot:

        await load_extensions()

        await bot.start(config.TOKEN)


# --------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())