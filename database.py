import aiosqlite
import os

DATABASE = "database/msno.db"


# Create database folder if it doesn't exist
os.makedirs("database", exist_ok=True)


async def create_tables():
    async with aiosqlite.connect(DATABASE) as db:

        # Daily Check-Ins
        await db.execute("""
        CREATE TABLE IF NOT EXISTS daily_checkins (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            username TEXT NOT NULL,

            date TEXT NOT NULL,

            prayer_answer TEXT,
            prayer_reason TEXT,

            sleep_answer TEXT,
            sleep_reason TEXT,

            exercise_answer TEXT,
            exercise_reason TEXT,

            agency_answer TEXT,
            agency_reason TEXT,

            lust_answer TEXT,
            lust_reason TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        await db.commit()


async def save_checkin(
    user_id,
    username,
    date,
    prayer_answer,
    prayer_reason,
    sleep_answer,
    sleep_reason,
    exercise_answer,
    exercise_reason,
    agency_answer,
    agency_reason,
    lust_answer,
    lust_reason,
):
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        INSERT INTO daily_checkins (

            user_id,
            username,
            date,

            prayer_answer,
            prayer_reason,

            sleep_answer,
            sleep_reason,

            exercise_answer,
            exercise_reason,

            agency_answer,
            agency_reason,

            lust_answer,
            lust_reason

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            username,
            date,

            prayer_answer,
            prayer_reason,

            sleep_answer,
            sleep_reason,

            exercise_answer,
            exercise_reason,

            agency_answer,
            agency_reason,

            lust_answer,
            lust_reason
        ))

        await db.commit()


async def has_submitted_today(user_id, date):
    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
        SELECT id
        FROM daily_checkins
        WHERE user_id = ?
        AND date = ?
        """, (user_id, date))

        result = await cursor.fetchone()

        return result is not None


async def get_user_stats(user_id):
    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
        SELECT *
        FROM daily_checkins
        WHERE user_id = ?
        ORDER BY date DESC
        """, (user_id,))

        return await cursor.fetchall()