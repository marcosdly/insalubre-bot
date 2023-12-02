import discord
from client import client
from commands.manage_friends import add_friend, remove_friend
from constants import Constants
from local.io import raw_access_db

async def on_message(message: discord.Message) -> None:
    db = raw_access_db()
    if client.user.id == message.author.id or message.author.id not in db["adminIds"]:
        return

    if message.content.startswith("T+add_amigo" + Constants.suffixes.sudo):
        await add_friend(message, sudo = True)
    elif message.content.startswith(cmd := "T+add_amigo"):
        await add_friend(message, sudo_command=cmd + Constants.suffixes.sudo)

    if message.content.startswith("T+remove_amigo" + Constants.suffixes.insecure):
        await remove_friend(message, sudo = True)
    elif message.content.startswith(cmd := "T+remove_amigo"):
        await remove_friend(message, sudo_command=cmd + Constants.suffixes.insecure)

