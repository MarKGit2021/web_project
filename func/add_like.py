from __future__ import annotations
from sqlalchemy import exc

from data.likes import Like
from data import db_session
"""не используется"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data.information import Information


def add_like(db, information: Information, user_id: int):
    information.points = information.points + 1
    db.commit()
    like = Like()
    like.user_id = user_id
    like.information_id = information.id
    try:
        db.add(like)
        db.commit()
    except exc.IntegrityError:
        db.rollback()
    db.commit()


def delete_like(db, information: Information, user_id: int):
    information.points -= 1
    like = db.query(Like).filter(Like.information_id == information.id, Like.user_id == user_id)[0]
    db.delete(like)