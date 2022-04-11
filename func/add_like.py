from sqlalchemy import exc

# from data.information import Information
from data.likes import Like
# from data import db_session


def add_like(db, information, user_id):
    # db = db_session.create_session()
    information.points += 1
    like = Like()
    like.user_id = user_id
    like.information_id = information.id
    try:
        db.add(like)
        db.commit()
    except exc.IntegrityError:
        db.rollback()
    db.commit()
    db.close()
