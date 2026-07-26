import discord
from datetime import datetime
from zoneinfo import ZoneInfo

import config
from database import save_checkin, has_submitted_today
from ui.embeds import create_checkin_embed


class DailyCheckInModal(discord.ui.Modal, title="🌙 Daily Check-In"):

    prayer = discord.ui.TextInput(
        label="1. Prayed all 5 prayers?",
        placeholder="Example: Yes - Prayed all 5 on time.",
        required=True,
        max_length=250,
    )

    sleep = discord.ui.TextInput(
        label="2. Slept 8+ hours?",
        placeholder="Example: No - Only slept 6 hours.",
        required=True,
        max_length=250,
    )

    exercise = discord.ui.TextInput(
        label="3. Exercised?",
        placeholder="Example: Yes - Walked 10k steps.",
        required=True,
        max_length=250,
    )

    agency = discord.ui.TextInput(
        label="4. Worked on your agency?",
        placeholder="Example: Yes - Continued editing my VSL.",
        required=True,
        max_length=250,
    )

    lust = discord.ui.TextInput(
        label="5. Stayed away from lust?",
        placeholder="Example: Yes - Avoided all triggers.",
        required=True,
        max_length=250,
    )

    def parse_answer(self, text: str):
        text = text.strip()

        if text.lower().startswith("yes"):
            answer = "✅ Yes"
            reason = text[3:].lstrip(" -:")
        elif text.lower().startswith("no"):
            answer = "❌ No"
            reason = text[2:].lstrip(" -:")
        else:
            answer = "❓ Unknown"
            reason = text

        if reason == "":
            reason = "No reason provided."

        return answer, reason

    async def on_submit(self, interaction: discord.Interaction):

        today = datetime.now(
            ZoneInfo(config.TIMEZONE)
        ).strftime("%Y-%m-%d")

        if await has_submitted_today(interaction.user.id, today):
            await interaction.response.send_message(
                "✅ You've already completed today's check-in.",
                ephemeral=True,
            )
            return

        prayer_answer, prayer_reason = self.parse_answer(self.prayer.value)
        sleep_answer, sleep_reason = self.parse_answer(self.sleep.value)
        exercise_answer, exercise_reason = self.parse_answer(self.exercise.value)
        agency_answer, agency_reason = self.parse_answer(self.agency.value)
        lust_answer, lust_reason = self.parse_answer(self.lust.value)

        await save_checkin(
            interaction.user.id,
            interaction.user.display_name,
            today,
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
        )

        embed = create_checkin_embed(
            interaction.user.display_name,
            today,
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
        )

        await interaction.response.send_message(
            "✅ Your Daily Check-In has been submitted!",
            ephemeral=True,
        )

        await interaction.channel.send(embed=embed)