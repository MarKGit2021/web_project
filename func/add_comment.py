from sqlalchemy import exc

# from data.information import Information
from data.comments import Comment
# from data import db_session


def add_comment(db, text: str, information_id: int, user_id: int):
    """
    Метод, добавляющий комментарий в базу\n
    :param db: база
    :param text: str - текст комментария
    :param information_id:int - id информации, к которой добавляют
    :param user_id: int - id, кто добавляет
    :return:
    """
    comment = Comment()
    comment.text = text
    comment.information_id = information_id
    comment.user_id = user_id
    db.add(comment)
    db.commit()
