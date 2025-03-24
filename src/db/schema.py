import string
from typing import Any, NamedTuple, final, override

from sqlalchemy import engine, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# region CUSTOM TYPES
class MusicBotCommands(NamedTuple):
  play: str
  pause: str
  resume: str
  stop: str
  skip: str
  nowplaying: str
  queue: str
  search: str


@final
class SQLType_MusicBotCommands(types.TypeDecorator[str]):
  impl = types.TEXT
  cache_ok = True
  separator = '\0'
  """List separator that should be unique and not conflict with any prefix or suffix"""

  @override
  def process_bind_param(
    self, value: str | None, dialect: engine.Dialect
  ) -> MusicBotCommands | None:
    if value is None:
      return
    value = value.strip(string.whitespace + string.punctuation)
    if value == '':
      raise ValueError(
        'string is empty or contains only invalid characters (whitespace and punctuation)'
      )
    return MusicBotCommands(*value.split(self.separator))

  @override
  def process_result_value(
    self, value: Any | None, dialect: engine.Dialect
  ) -> str | None:
    if value is None:
      return
    if not isinstance(value, MusicBotCommands):
      raise TypeError("value is not an instance of 'MusicBotCommands'")
    return self.separator.join(value)


# endregion CUSTOM TYPES


class BaseTable(DeclarativeBase):
  pass


class MusicBot(BaseTable):
  __tablename__: str = 'music_bot'

  user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
  prefix: Mapped[str]
  commands: Mapped[MusicBotCommands] = mapped_column(SQLType_MusicBotCommands)
