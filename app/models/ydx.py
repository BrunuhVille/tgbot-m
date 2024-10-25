import logging
import random
import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Float,
    BigInteger,
    Text,
    TIMESTAMP,
    SmallInteger,
    DateTime,
    func,
)
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base


logger = logging.getLogger("main")


class ZqYdx(Base):
    __tablename__ = "zqydx"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_bouns: Mapped[int] = mapped_column(Integer)
    high_times: Mapped[int] = mapped_column(Integer)
    low_times: Mapped[int] = mapped_column(Integer)
    dx: Mapped[int] = mapped_column(Integer, nullable=True)
    bet_switch: Mapped[int] = mapped_column(Integer)
    bet_mode: Mapped[str] = mapped_column(String(8))
    kp_switch: Mapped[int] = mapped_column(Integer)
    rel_betbonus: Mapped[int] = mapped_column(Integer)
    lose_times: Mapped[int] = mapped_column(Integer)
    win_times: Mapped[int] = mapped_column(Integer)
    sum_losebonus: Mapped[int] = mapped_column(Integer)
    message_id: Mapped[int] = mapped_column(Integer, nullable=True)
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime)

    @classmethod
    def init(cls, session: AsyncSession):
        self = cls(
            start_bouns=500,
            high_times=0,
            low_times=0,
            bet_point=1,
            bet_switch=0,
            bet_mode="A",
            kp_switch=0,
            rele_betbouns=0,
            lose_times=0,
            win_times=0,
            sum_losebouns=0,
            update_time=func.now(),
        )
        session.add(self)
        return self


class YdxHistory(Base):
    __tablename__ = "zqydx_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dx: Mapped[int] = mapped_column(Integer)
