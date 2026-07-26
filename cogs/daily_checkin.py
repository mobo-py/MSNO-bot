import discord
from discord.ext import commands
from discord import app_commands

import config
from ui.buttons import DailyCheckInView


async def post_daily_checkin(channel):

    role = channel.guild.get_role(config.MASTERMIND_ROLE_ID)

    embed = discord.Embed(
        title="🌙 Daily Check-In",
        description=(
            "Complete your daily check-in before going to sleep.\n\n"
            "Click **Complete Check-In** below."
        ),
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="Today's Checklist",
        value=(
            "🙏 Pray all 5 prayers\n"
            "😴 Sleep 8+ hours\n"
            "🏋️ Exercise\n"
            "💼 Work on your agency\n"
            "🛡️ Stay away from lust"
        ),
        inline=False
    )

    await channel.send(
        content=role.mention if role else None,
        embed=embed,
        view=DailyCheckInView()
    )


class DailyCheckIn(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="postcheckin",
        description="Post today's Daily Check-In."
    )
    async def postcheckin(
        self,
        interaction: discord.Interaction
    ):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You don't have permission to use this.",
                ephemeral=True
            )
            return

        channel = self.bot.get_channel(config.DAILY_CHANNEL_ID)

        print(channel)

        if channel:
            print(channel.name)
            print(channel.id)

            me = interaction.guild.get_member(self.bot.user.id)
            print(channel.permissions_for(me))

        if channel is None:
            await interaction.response.send_message(
                "Daily Check-In channel not found.",
                ephemeral=True
            )
            return

        await post_daily_checkin(channel)

        await interaction.response.send_message(
            "✅ Posted today's Daily Check-In.",
            ephemeral=True
        )
    @postcheckin.error
    async def postcheckin_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        import traceback

        traceback.print_exception(type(error), error, error.__traceback__)

        if not interaction.response.is_done():
            await interaction.response.send_message(
                f"Error:\n```{error}```",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(DailyCheckIn(bot))