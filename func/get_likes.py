# from sqlalchemy import exc

# from data.information import Information
from data.likes import Like

# from data import db_session


def get_likes(db, information_id: int):
    """
    Метод, выдающий количество лайков у информации\n
    :param db: База данных, с которой работаем
    :param information_id:
    :return:
    """
    # db = db_session.create_session()
    likes = len(list(db.query(Like).filter(Like.information_id == information_id)))
    # db.close()
    return likes
