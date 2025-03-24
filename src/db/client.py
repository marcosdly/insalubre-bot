from pathlib import Path

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if __debug__:
  db_path = Path('persistent_data.dev.db')
else:
  db_path = Path('persistent_data.prod.db')

engine = create_async_engine(f'sqlite+aiosqlite://{db_path.absolute()}', echo=__debug__)
async_session = async_sessionmaker(engine)
