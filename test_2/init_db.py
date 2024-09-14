import asyncio
from random import randint

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine
from models import Level, Player, Prize


async def init_db():
    async with AsyncSession(bind=engine) as db:
        await db.execute(insert(Player).returning(Player))
        await db.execute(insert(Level).values(title=f"test_{randint(1, 100000)}"))
        await db.execute(insert(Prize).values(title=f"test_{randint(1, 100000)}"))
        await db.commit()


if __name__ == "__main__":
    asyncio.run(init_db())
