from pathlib import Path

from sqlalchemy import create_engine

if __debug__:
  db_path = Path('persistent_data.dev.db')
else:
  db_path = Path('persistent_data.prod.db')

engine = create_engine(f'sqlite+aiosqlite://{db_path.absolute()}', echo=__debug__)
