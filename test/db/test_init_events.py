from typing import TYPE_CHECKING, Unpack

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.asyncio import AsyncEngine
from src.db.client import dbevent_create_schema

if TYPE_CHECKING:
  from sqlalchemy.dialects.sqlite.aiosqlite import AsyncAdapt_aiosqlite_connection
  from sqlalchemy.pool import ConnectionPoolEntry


@pytest_asyncio.fixture(loop_scope='session', scope='function')
async def async_engine():
  from sqlalchemy.ext.asyncio import create_async_engine

  return create_async_engine('sqlite+aiosqlite:///:memory:')


@pytest.mark.asyncio(loop_scope='session')
async def test_create_schema(async_engine: AsyncEngine):
  _called = False

  def run_event(
    *args: Unpack[tuple['AsyncAdapt_aiosqlite_connection', 'ConnectionPoolEntry']],
  ):
    nonlocal _called
    _called = True
    dbevent_create_schema(*args)

  event.listen(async_engine.sync_engine, 'first_connect', run_event)

  try:
    async with async_engine.begin() as _:
      # event will be called as soon as trying to create connection
      assert _called, 'event was not called'
      inspector = Inspector(async_engine.sync_engine)
      tables_should_exist = ['music_bot']

      # NOTE: metadata.create_all parameter 'checkfirst' is True, so schema creation
      # will not be forced in case tables already exist.
      # Pre-runtime tests of schema validation are a matter migration.
      for table_name in tables_should_exist:
        assert inspector.has_table(table_name), f"table does not exist: '{table_name}'"
  except Exception as err:
    pytest.fail(str(err))
