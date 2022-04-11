from sqlalchemy import exc

from data.likes import Like


def add_like(db, information, user_id):
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
