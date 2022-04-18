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
    inf = Information()
    inf.user_id = 1
    db.add(inf)
    db.commit()
    print(inf.id)
    inf.save_text('  Самая первая информация, которую мы сделали!  ', folder='../db/files/')
    # word = Word()
    # word.word = 'first information'
    word = db.query(Word).first()
    # db.add(word)
    # db.commit()
    # inf_by_word = InformationByWord()
    # inf_by_word.word = word
    # inf_by_word.information = inf
    # db.add(inf_by_word)
    # db.commit()
    print(word.all_information)