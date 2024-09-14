import os
import tempfile

import pandas as pd
from celery import Celery
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from database import sync_engine
from models import PlayerLevel
from settings import settings

celery_app: Celery = Celery(
    "background_tasks", broker=f"amqp://{settings.MQ_USER}:{settings.MQ_PASS}@{settings.MQ_HOST}:5672"
)
celery_app.autodiscover_tasks()


def make_tempfile(suffix=".csv", dir="/tmp"):  # noqa: S108
    _fhandle, fname = tempfile.mkstemp(suffix=suffix, dir=dir)
    return _fhandle, fname


@celery_app.task()
def make_csv_file():
    with Session(bind=sync_engine) as db:
        df = pd.DataFrame(
            [row.player_id, row.level.title, row.is_completed, len(row.levelprizes)]
            for row in (
                db.execute(
                    select(PlayerLevel)
                    .options(joinedload(PlayerLevel.level))
                    .options(joinedload(PlayerLevel.levelprizes))
                )
            )
            .unique()
            .scalars()
            .all()
        )
        df.columns = ["player_id", "level_title", "is_completed", "level_prize_counts"]
        _fhandle, fname = make_tempfile()
        df.to_csv(fname, sep="\t")
        print(df)
        # Send by EMAIL or S3
        os.remove(fname)
