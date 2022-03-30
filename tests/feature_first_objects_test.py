from data import db_session
from data.information import Information
from data.users import User

if __name__ == '__main__':
    # a = input().strip()
    db_session.global_init('first.db')
    db = db_session.create_session()
    # user = User()
    # user.name = 'User1'
    # user.surname = 'Users'
    # user.hashed_password = 'password'
    # user.email = 'email.email'
    # db.add(user)
    # db.commit()
    for user in db.query(User).all():
        print(user)
    inf = Information()
    inf.user_id = 1
    inf.folder = 'https/folder'
    db.add(inf)
    db.commit()
    user = db.query(User).first()
    print(user)
    print(user.information)
    print(inf.user)