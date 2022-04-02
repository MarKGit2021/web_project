from data import db_session
from data.comments import Comment
from data.information import Information
from data.users import User
from data.words import Word

if __name__ == '__main__':
    # a = input().strip()
    db_session.global_init('../db/db.db')
    db = db_session.create_session()
    inf = db.query(Information).first()