from sqlalchemy import exc

from data import db_session
from data.comments import Comment
from data.information import Information
from data.users import User
from data.words import Word

if __name__ == '__main__':
    # a = input().strip()
    db_session.global_init('../db/db.db')
    db = db_session.create_session()
    user = User()
    user.name = 'User1'
    user.surname = 'Users'
    user.hashed_password = 'password'
    user.email = 'email.email2'
    try:
        db.add(user)
        db.commit()
    except exc.IntegrityError:
        db.rollback()
    for user in db.query(User).all():
        print(user)
    inf = Information()
    inf.user_id = 1
    db.add(inf)
    db.commit()
    inf.save_text('text', '../templates/files/')
    word = Word()
    word.word = 'text'
    db.add(word)
    db.commit()
    word.append_information(inf, db=db)

    user = db.query(User).first()
    # inf = db.query(Information).all()[
    print(user)
    print(user.information)
    # print(inf.user)
    # word = db.query(Word).first()
    # word.information.append(inf)
    # db.commit()
    # print(user.comments)
    # print(comment.user)
