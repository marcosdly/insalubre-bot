if __name__ == "__main__":
    # Try not to initialize Constants after logging.
    # TODO Better logging module definition other than top level logic and variables
    from constants import Constants
    Constants.initialize()

    from client import client
    from events.on_message import on_message
    from events.on_voice_state_update import on_voice_state_update

    client.event(on_message)
    client.event(on_voice_state_update)

    from local.io import get_secrets
    secrets = get_secrets()

    client.run(secrets["discordToken"])
