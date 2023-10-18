import discord
from client import client
from commands.manage_friends import add_friend, remove_friend
from constants import sudo_suffix, insecure_suffix
from local.io import raw_access_db

async def on_message(message: discord.Message) -> None:
    db = raw_access_db()
    if client.user.id == message.author.id or message.author.id not in db["adminIds"]:
        return

    if message.content.startswith((cmd := "T+add_amigo") + sudo_suffix):
        await add_friend(message, cmd, sudo = True)
    elif message.content.startswith(cmd := "T+add_amigo"):
        await add_friend(message, cmd)

    if message.content.startswith((cmd := "T+remove_amigo") + insecure_suffix):
        await remove_friend(message, cmd, sudo = True)
    elif message.content.startswith(cmd := "T+remove_amigo"):
        await remove_friend(message, cmd)
    
                
