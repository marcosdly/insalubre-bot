import discord
from client import client
from commands.manage_friends import add_friend, remove_friend
from constants import Constants
from local.io import raw_access_db
from log import command_response_logger

async def on_message(message: discord.Message) -> None:
    db = raw_access_db()
    if client.user.id == message.author.id or message.author.id not in db["adminIds"]:
        return

    if message.content.startswith(cmd := "T+add_amigo" + Constants.suffixes.sudo):
        if message.mention_everyone:
            command_response_logger.info(f"User {message.author.name} ({message.author.id}) called {cmd} mentioning @everyone")
        else:
            command_response_logger.info(message.content)
        await add_friend(message, sudo = True)
    elif message.content.startswith(cmd := "T+add_amigo"):
        command_response_logger.info(message.content)
        await add_friend(message, sudo_command=cmd + Constants.suffixes.sudo)

    if message.content.startswith(cmd := "T+remove_amigo" + Constants.suffixes.insecure):
        if message.mention_everyone:
            command_response_logger.info(f"User {message.author.name} ({message.author.id}) called {cmd} mentioning @everyone")
        else:
            command_response_logger.info(message.content)
        await remove_friend(message, sudo = True)
    elif message.content.startswith(cmd := "T+remove_amigo"):
        command_response_logger.info(message.content)
        await remove_friend(message, sudo_command=cmd + Constants.suffixes.insecure)

