from pprint import pprint

import nextcord
from nextcord.ext import commands

GUILD_IDS: set[int] = set()

bot = commands.Bot(lazy_load_commands=False)


@bot.event
async def on_ready():
  for guild in bot.guilds:
    GUILD_IDS.add(guild.id)
  pprint(GUILD_IDS, indent=2, underscore_numbers=True)
  pprint(vars(bot))

  from src.db.client import engine
  from src.db.schema import BaseTable

  async with engine.begin() as conn:
    await conn.run_sync(BaseTable.metadata.create_all)
