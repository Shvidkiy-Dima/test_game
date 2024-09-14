from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from settings import settings

engine = create_async_engine(settings.DB_URL)
sync_engine = create_engine(settings.ALEMBIC_DB_URL)
