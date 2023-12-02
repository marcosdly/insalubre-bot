import discord
from local.io import access_db

async def add_friend(message: discord.Message, *, sudo_command: str | None = None, sudo: bool = False) -> None:
    """If `sudo` is `True` you don't need to specify a `sudo_command`."""
    if sudo and message.mention_everyone:
        with access_db() as db:
            db["whatsapp"]["notify"] = [x.id for x in message.guild.members]
        await message.channel.send("Agora todo mundo está na sua lista de amigos (nem um pouco suspeito).", reference=message.to_reference())
        return
    elif message.mention_everyone:
        if sudo_command is None:
            raise ValueError("A command to tell the user what to run in order to do the distructive action is necessary.")
        await message.channel.send(f"Vocẽ não pode adicionar todo mundo de uma vez só à sua lista de amigos (medida anti-estupidez). Para fazer isso, utilize o comando {sudo_command}.", reference=message.to_reference())
        return
    
    if len(message.mentions) == 0:
        await message.channel.send("Mencione as pessoas que deseja adicionar como amigas.", reference=message.to_reference())
        return

    with access_db() as db:
        already_in = set(db["whatsapp"]["notify"])
        trying_to_add = set(x.id for x in message.mentions)
        unique = trying_to_add.difference(already_in)
        if len(unique) == 0:
            await message.channel.send("Todos os usuários citados já estão na lista de amigos.", reference=message.to_reference())
            return
        db["whatsapp"]["notify"].extend(unique)
        if len(unique) < len(trying_to_add):
            await message.channel.send("Amigos adicionados com sucesso! "
                                    f"{len(trying_to_add) - len(unique)} usuários já estavam na lista de amigos.",
                                    reference=message.to_reference())
            return
        await message.channel.send("Amigos adicionados com sucesso!", reference=message.to_reference())
        return
    
async def remove_friend(message: discord.Message, *, sudo_command: str | None = None, sudo: bool = False) -> None:
    if sudo and message.mention_everyone:
        with access_db() as db:
            db["whatsapp"]["notify"].clear()
            await message.channel.send("Você removeu todo mundo da sua lista de amigos (equivalente a ser cinéfilo).", reference=message.to_reference())
            return
    elif message.mention_everyone:
        if sudo_command is None:
            raise ValueError("A command to tell the user what to run in order to do the distructive action is necessary.")
        await message.channel.send(f"Você não pode remover todo mundo da sua lista de amigos, para fazer isso, utilize o comando {sudo_command}.", reference=message.to_reference())
        return
    
    if len(message.mentions) == 0:
        await message.channel.send("Mencione as pessoas que deseja remover da sua lista de amigos.", reference=message.to_reference())
        return

    with access_db() as db:
        already_in = set(db["whatsapp"]["notify"])
        trying_to_remove = set(x.id for x in message.mentions)
        valid = already_in.intersection(trying_to_remove)
        if len(valid) == 0:
            await message.channel.send("Todos os usuários que você mencionou já não estão na sua lista de amigos.", reference=message.to_reference())
            return
        db["whatsapp"]["notify"] = list(already_in.difference(valid))
        await message.channel.send(f"{len(valid)} usuários removidos da sua lista de amigos.", reference=message.to_reference())
        return
