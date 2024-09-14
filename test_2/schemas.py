from uuid import UUID

from pydantic import BaseModel, Field


class AddPrizeSchema(BaseModel):
    player_id: UUID
    prize_id: UUID
    level_id: UUID
    score: int = Field(ge=0)


class AddPrizeResponseSchema(BaseModel):
    level_prize_id: UUID
    prize_title: str
