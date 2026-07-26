import discord

from ui.modals import DailyCheckInModal


class DailyCheckInView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Complete Check-In",
        emoji="🌙",
        style=discord.ButtonStyle.primary,
        custom_id="daily_checkin_button"
    )
    async def complete_checkin(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(DailyCheckInModal())  