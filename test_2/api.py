from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from background_tasks import make_csv_file
from deps import get_db
from models import Level, LevelPrize, Player, PlayerLevel, Prize
from schemas import AddPrizeResponseSchema, AddPrizeSchema

router = APIRouter()


@router.post("/prize/", response_model=AddPrizeResponseSchema)
async def add_prize(data_in: AddPrizeSchema, db: AsyncSession = Depends(get_db)) -> AddPrizeResponseSchema:
    player = (await db.execute(select(Player).where(Player.id == data_in.player_id))).scalars().first()
    prize = (await db.execute(select(Prize).where(Prize.id == data_in.prize_id))).scalars().first()
    level = (await db.execute(select(Level).where(Level.id == data_in.level_id))).scalars().first()
    if not all((prize, player, level)):
        raise HTTPException(status_code=404, detail="Not Found")

    player_level = (
        (
            await db.execute(
                select(PlayerLevel).where(PlayerLevel.level_id == level.id, PlayerLevel.player_id == player.id)
            )
        )
        .scalars()
        .first()
    )

    if player_level is None:
        player_level = (
            (
                await db.execute(
                    insert(PlayerLevel)
                    .values(
                        player_id=player.id,
                        level_id=level.id,
                        completed=datetime.utcnow(),
                        is_completed=True,
                        score=data_in.score,
                    )
                    .returning(PlayerLevel)
                )
            )
            .scalars()
            .first()
        )

    level_prize = (
        (
            await db.execute(
                insert(LevelPrize)
                .values(
                    player_level_id=player_level.id,
                    prize_id=prize.id,
                    received=datetime.utcnow(),
                )
                .returning(LevelPrize)
            )
        )
        .scalars()
        .first()
    )

    await db.commit()
    return AddPrizeResponseSchema(level_prize_id=level_prize.id, prize_title=prize.title)


@router.get("/info/")
async def get_total_info():
    make_csv_file.delay()
    return Response(status_code=200)
