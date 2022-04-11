# from sqlalchemy import exc

# from data.information import Information
from data.likes import Like

# from data import db_session


def get_likes(db, information_id: int, user_id: int):
    # db = db_session.create_session()
    likes = len(list(db.query(Like).filter(Like.information_id == information_id)))
    is_liked = len(list(db.query(Like).filter(Like.information_id == information_id, Like.user_id == user_id))) != 0
    db.close()
    return likes, is_liked
