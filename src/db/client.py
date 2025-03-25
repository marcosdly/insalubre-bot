from pathlib import Path
from typing import TYPE_CHECKING, Unpack

if TYPE_CHECKING:
  from sqlalchemy.dialects.sqlite.aiosqlite import AsyncAdapt_aiosqlite_connection
  from sqlalchemy.pool import ConnectionPoolEntry

from sqlalchemy.ext.asyncio import create_async_engine

# region Init ORM

if __debug__:
  db_path = Path('persistent_data.dev.db')
else:
  db_path = Path('persistent_data.prod.db')

async_engine = create_async_engine(
  f'sqlite+aiosqlite:///{db_path.absolute()}', echo=__debug__
)

# endregion


# region Event callbacks


def dbevent_create_schema(
  *_: Unpack[tuple['AsyncAdapt_aiosqlite_connection', 'ConnectionPoolEntry']],
):
  from src.db.schema import BaseTable

  global async_engine

  BaseTable.metadata.create_all(async_engine.sync_engine)


# endregion
