# from sqlalchemy import exc

# from data.information import Information
from data.comments import Comment
# from data.likes import Like

from data import db_session


def get_comment(db, information_id: int):
    # db = db_session.create_session()
    comment = [i.get_comment_information()
               for i in db.query(Comment).filter(Comment.information_id == information_id)]
    db.close()
    return comment
