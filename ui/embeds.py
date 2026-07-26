import discord


def create_checkin_embed(
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

    embed = discord.Embed(
        title=f"🌙 {username}'s Daily Check-In",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="🙏 Prayer",
        value=f"{prayer_answer}\n{prayer_reason}",
        inline=False
    )

    embed.add_field(
        name="😴 Sleep",
        value=f"{sleep_answer}\n{sleep_reason}",
        inline=False
    )

    embed.add_field(
        name="🏋️ Exercise",
        value=f"{exercise_answer}\n{exercise_reason}",
        inline=False
    )

    embed.add_field(
        name="💼 Agency",
        value=f"{agency_answer}\n{agency_reason}",
        inline=False
    )

    embed.add_field(
        name="🛡️ Lust",
        value=f"{lust_answer}\n{lust_reason}",
        inline=False
    )

    embed.set_footer(text=date)

    return embed