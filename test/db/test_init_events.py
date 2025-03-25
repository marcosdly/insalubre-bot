from typing import TYPE_CHECKING, Any, Unpack

import pytest
import pytest_asyncio
from sqlalchemy import event, inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.inspection import Inspectable
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

  tables_should_exist = ['music_bot']

  def sync_run_inspection(conn_inner: Inspectable[Any]):
    inspector: Inspector = inspect(conn_inner)
    # NOTE: metadata.create_all parameter 'checkfirst' is True, so schema creation
    # will not be forced in case tables already exist.
    # Pre-runtime tests of schema validation are a matter migration.
    for table_name in tables_should_exist:
      assert inspector.has_table(table_name) is True, (
        f"table does not exist: '{table_name}'"
      )

  try:
    async with async_engine.begin() as conn:
      # event will be called as soon as trying to create connection
      assert _called is True, 'event was not called'
      await conn.run_sync(sync_run_inspection)
  except Exception as err:
    pytest.fail(str(err))
