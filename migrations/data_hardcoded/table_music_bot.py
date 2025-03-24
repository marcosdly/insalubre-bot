from collections.abc import Sequence

from src.db.schema import MusicBot, MusicBotCommands

DATA: Sequence[MusicBot] = [
  MusicBot(
    description='FredBoat',
    user_id=184405253028970496,
    uses_slash_commands=True,
    commands=MusicBotCommands(queue='list', nowplaying='nowplaying'),
  ),
]
