from sqlalchemy import exc

# from data.information import Information
from data.comments import Comment
# from data import db_session


def add_comment(db, text: str, information_id: int, user_id: int):
    # db = db_session.create_session()
    comment = Comment()
    comment.text = text
    comment.information_id = information_id
    comment.user_id = user_id
    db.add(comment)
    db.commit()
    db.close()
