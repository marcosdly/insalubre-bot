import discord
from local.io import raw_access_db
from whatsapp import green_api

async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    db = raw_access_db()
    if member.id not in db["whatsapp"]["notify"]:
        return
    
    if before.channel is None and after.channel is not None:
        green_api.sending.sendMessage(
            db["whatsapp"]["targetGroupId"],
            f"Brother {member.nick if member.nick else member.name} entrou no canal {after.channel.name} no servidor {after.channel.guild.name}."
        )
        return