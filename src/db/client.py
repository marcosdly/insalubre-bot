from collections.abc import Sequence
from pathlib import Path

from sqlalchemy import event, insert, select
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import ConnectionPoolEntry

if __debug__:
  db_path = Path('persistent_data.dev.db')
else:
  db_path = Path('persistent_data.prod.db')

engine = create_async_engine(
  f'sqlite+aiosqlite:///{db_path.absolute()}', echo=__debug__
)
async_session = async_sessionmaker(engine)


@event.listens_for(engine.sync_engine, 'first_connect')
def ensure_music_bot_data(conn: DBAPIConnection, conn_record: ConnectionPoolEntry):
  from ...migrations.data_hardcoded.table_music_bot import DATA
  from .schema import MusicBot

  cursor = conn.cursor()
  select_stmt = select(MusicBot.user_id)
  primary_keys: Sequence[int] = cursor.execute(select_stmt)
  data_intersection = [row for row in DATA if row.user_id not in primary_keys]
  if len(data_intersection) == 0:
    return

  insert_stmt = insert(MusicBot).values(data_intersection)
  cursor.execute(insert_stmt)

  conn.commit()
  cursor.close()
  conn.close()
