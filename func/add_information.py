from sqlalchemy import exc

from data.information import Information
from data.words import Word
from data import db_session


def add_information(db, text, word: str, user_id: int, words: str = None):
    """
    Метод, который добавляет информацию в базу данных
    :param db: база
    :param text: bytes or str - содержимое информации
    :param word: str -главное слово для поиска
    :param user_id: int - кто создал
    :param words: Optional[str] - дополнительные слова
    :return:
    """
    if words is None:
        words = []
    else:
        words = words.strip().lower().split('; ')
    # db = db_session.create_session()
    information = Information()
    information.user_id = user_id
    db.add(information)
    db.commit()
    print('tyt', information.id)
    information.save_text(text)
    db.commit()
    for i in [word] + words:
        if i.strip() != '':
            new_word = Word()
            new_word.word = i.strip().lower()
            # db.add(new_word)
            try:
                db.add(new_word)
                db.commit()
            except exc.IntegrityError:
                db.rollback()
                new_word = db.query(Word).filter(Word.word == i.strip().lower())[0]
            information.append_word(new_word, db=db)
            db.commit()
    db.close()
    return True