import discord

intents = discord.Intents.default()

intents.messages = True
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)