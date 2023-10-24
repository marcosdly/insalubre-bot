from os.path import isfile, join
from shutil import copyfile

from client import client
from events.on_message import on_message
from events.on_voice_state_update import on_voice_state_update
from local.io import ProjectFolders, get_secrets


@client.event
async def on_connect():
    print("Bot successfully started and connected!")
    print(
        f"Username: {client.user.name}",
        f"ID: {client.user.id}",
        f"Locale: {client.user.locale}",
        f"Verified: {client.user.public_flags.verified_bot}",
        sep="\n"
    )

    if not isfile(dest := join(ProjectFolders.root, "db.json")):
        copyfile(join(ProjectFolders.templates, "db.json"), dest)

client.event(on_message)
client.event(on_voice_state_update)

if __name__ == "__main__":
    secrets = get_secrets()
    client.run(secrets["discordToken"])
