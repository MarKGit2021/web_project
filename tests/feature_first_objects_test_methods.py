from data import db_session
from data.comments import Comment
from data.users import User

if __name__ == '__main__':
    db_session.global_init('../db/db.db')
    db = db_session.create_session()
    user = db.query(User).first()
    comment = db.query(Comment).first()
    print(comment.get_comment_information())
    print(user.get_user_information())
    print(user.comments)
    print(comment.user)
