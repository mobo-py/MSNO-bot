from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import config
from cogs.daily_checkin import post_daily_checkin

scheduler = AsyncIOScheduler(
    timezone=config.TIMEZONE
)


async def send_daily_checkin(bot):

    channel = bot.get_channel(config.DAILY_CHANNEL_ID)

    if channel is None:
        print("Daily Check-In channel not found.")
        return

    await post_daily_checkin(channel)


async def start_scheduler(bot):

    if scheduler.running:
        return

    scheduler.add_job(
        send_daily_checkin,
        CronTrigger(
            hour=config.CHECKIN_HOUR,
            minute=config.CHECKIN_MINUTE
        ),
        args=[bot],
        id="daily_checkin",
        replace_existing=True
    )

    scheduler.start()

    print("✓ Scheduler Started")