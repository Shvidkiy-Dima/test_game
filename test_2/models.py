from uuid import uuid4

from sqlalchemy import UUID, Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship


class Base(DeclarativeBase):
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BaseModel(Base):
    __abstract__ = True

    id = mapped_column(UUID, primary_key=True, index=True, nullable=False, default=uuid4)


class Player(BaseModel):
    playerlevels = relationship("PlayerLevel", back_populates="player")


class Level(BaseModel):
    title = mapped_column(String(100), nullable=False)
    order = mapped_column(Integer, default=0, nullable=False)

    playerlevels = relationship("PlayerLevel", back_populates="level")


class Prize(BaseModel):
    title = mapped_column(Text, nullable=False)

    levelprizes = relationship("LevelPrize", back_populates="prize")


class PlayerLevel(BaseModel):
    __table_args__ = (CheckConstraint("score >= 0"),)

    player_id = mapped_column(UUID, ForeignKey("player.id"), nullable=False, index=True)
    level_id = mapped_column(UUID, ForeignKey("level.id"), nullable=False, index=True)

    player = relationship("Player", back_populates="playerlevels")
    level = relationship("Level", back_populates="playerlevels")

    completed = mapped_column(DateTime(timezone=False))
    is_completed = mapped_column(Boolean, nullable=False, default=False)
    score = mapped_column(Integer, nullable=False, default=0)

    levelprizes = relationship("LevelPrize", back_populates="player_level")


class LevelPrize(BaseModel):
    received = mapped_column(DateTime(timezone=False))
    prize_id = mapped_column(UUID, ForeignKey("prize.id"), nullable=False, index=True)
    player_level_id = mapped_column(UUID, ForeignKey("playerlevel.id"), nullable=False, index=True)

    player_level = relationship("PlayerLevel", back_populates="levelprizes")
    prize = relationship("Prize", back_populates="levelprizes")
