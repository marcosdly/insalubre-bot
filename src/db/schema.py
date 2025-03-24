import string
import uuid
from typing import Any, NamedTuple, Never, Optional, final, override

from sqlalchemy import engine, types
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# region Type: MusicBotCommands
class MusicBotCommands(NamedTuple):
  play: str = 'play'
  pause: str = 'pause'
  resume: str = 'resume'
  stop: str = 'stop'
  skip: str = 'skip'
  nowplaying: str = 'np'
  queue: str = 'q'
  search: str = 'search'


@final
class SQLType_MusicBotCommands(types.TypeDecorator[str]):
  impl = types.TEXT
  cache_ok = True
  separator = '\0'
  """List separator that should be unique and not conflict with any prefix or suffix"""

  def __init__(self, cache_hash: Never = ...):  # pyright: ignore[reportArgumentType]
    super().__init__()
    self.cache_hash = uuid.uuid4().int

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


class BaseTable(AsyncAttrs, DeclarativeBase):
  type_annotation_map: dict[type[Any], type[types.TypeEngine[Any]]] = {
    MusicBotCommands: SQLType_MusicBotCommands,
  }


class MusicBot(BaseTable):
  __tablename__: str = 'music_bot'

  user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
  prefix: Mapped[Optional[str]] = mapped_column(default=None)
  description: Mapped[Optional[str]] = mapped_column(default=None)
  uses_slash_commands: Mapped[bool] = mapped_column(default=False)
  commands: Mapped[MusicBotCommands] = mapped_column(default=MusicBotCommands())
  voice_channel_id: Mapped[Optional[int]] = mapped_column(default=None)
