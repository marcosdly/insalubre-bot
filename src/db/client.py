# from collections.abc import Sequence
from pathlib import Path

# from sqlalchemy import  insert, select
from typing import TYPE_CHECKING, Unpack

if TYPE_CHECKING:
  from sqlalchemy.dialects.sqlite.aiosqlite import AsyncAdapt_aiosqlite_connection
  from sqlalchemy.pool import ConnectionPoolEntry

from sqlalchemy.ext.asyncio import (
  async_sessionmaker,
  create_async_engine,
)

# region Init ORM

if __debug__:
  db_path = Path('persistent_data.dev.db')
else:
  db_path = Path('persistent_data.prod.db')

engine = create_async_engine(
  f'sqlite+aiosqlite:///{db_path.absolute()}', echo=__debug__
)
async_session = async_sessionmaker(engine)

# endregion


# region Event callbacks


def dbevent_create_schema(
  *_: Unpack[tuple['AsyncAdapt_aiosqlite_connection', 'ConnectionPoolEntry']],
):
  import asyncio

  async def create_schema():
    from src.db.schema import BaseTable

    global engine

    async with engine.begin() as conn:
      await conn.run_sync(BaseTable.metadata.create_all)

  with asyncio.Runner(debug=__debug__, loop_factory=asyncio.new_event_loop) as runner:
    runner.run(create_schema())


# endregion
