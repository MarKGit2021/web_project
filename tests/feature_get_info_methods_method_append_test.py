from data import db_session
from data.comments import Comment
from data.information import Information
from data.users import User
from data.words import Word
from data.information_by_word import InformationByWord

if __name__ == '__main__':
    # a = input().strip()
    db_session.global_init('../db/db.db')
    db = db_session.create_session()
    word = db.query(Word).first()
    information = db.query(Information).first()
    print()
    print(word.all_information)
    print(information.all_words)
    information.append_word(word, db)
    print()
    print(word.all_information)
    print(information.all_words)
    word.append_information(information, db)
    print()
    print(word.all_information)
    print(information.all_words)
