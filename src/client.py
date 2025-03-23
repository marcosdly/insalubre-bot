from pprint import pprint

import nextcord
from nextcord.ext import commands

bot = commands.Bot(lazy_load_commands=False)


@bot.event
async def on_ready():
  pprint(vars(bot))
