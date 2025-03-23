import nextcord
from nextcord.ext import commands
from src.client import bot


@bot.slash_command('ping', 'Testar reposta', guild_ids=[1026408691873894430])
async def ping(interaction: nextcord.Interaction[commands.Bot]):
  _ = await interaction.send('pong!')
