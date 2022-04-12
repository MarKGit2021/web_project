# from sqlalchemy import exc

# from data.information import Information
from data.likes import Like

# from data import db_session


def get_likes(db, information_id: int):
    # db = db_session.create_session()
    likes = len(list(db.query(Like).filter(Like.information_id == information_id)))
    # db.close()
    return likes
