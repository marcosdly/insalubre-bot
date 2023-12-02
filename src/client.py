import discord

intents = discord.Intents.default()

intents.messages = True
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_connect():
    print(
        f"{client.user.name=}",
        # f"{client.user.id=}",
        f"{client.user.bot=}",
        f"{client.user.locale=}",
        f"{client.user.created_at=}",
        f"{client.user.display_name=}",
        f"{client.user.global_name=}",
        f"{client.user.mfa_enabled=}",
        f"{client.user.verified=}",
        f"{client.application.name=}",
        # f"{client.application.id=}",
        f"{client.application.owner.name=}",
        # f"{client.application.owner.id=}",
        sep="\n"
    )

