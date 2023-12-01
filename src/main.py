from constants import Constants
from local.io import get_secrets

if __name__ == "__main__":
    Constants.initialize()

    from client import client

    secrets = get_secrets()
    client.run(secrets["discordToken"])
