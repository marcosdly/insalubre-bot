def main():
  import asyncio
  import os
  import sys

  import src.commands.music_aggregator
  from src.client import bot

  bot.run(os.environ['DISCORD_API_KEY'])


if __name__ == '__main__':
  main()
