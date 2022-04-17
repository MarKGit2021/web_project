from __future__ import annotations
from typing import TYPE_CHECKING

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

if TYPE_CHECKING:
    from data.information import Information
from data.information_by_word import InformationByWord

from logger import Logger


# Этот класс, в принципе, тоже можно будет вырезать.
# Он нужен для того, чтобы в случае многоразового использования слова использовать меньше памяти
class Word(SqlAlchemyBase):
    __tablename__ = 'words'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    word = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    all_information = orm.relation("InformationByWord", back_populates='word')

    def __str__(self):
        return f"Слово id: {self.id}, word: {self.word}"

    def __repr__(self):
        return f'Слово(id: {self.id})'

    def append_information(self, information: Information, db):
        """
        Метод, который добавляет к слову информацию
        :param information: Information (информация, которую добавляем)
        :param db: База данных, с которой работаем.
        :return: None
        """
        if list(db.query(InformationByWord).filter(InformationByWord.word_id == self.id,
                                                       InformationByWord.information_id == information.id)):
            info = list(db.query(InformationByWord).filter(InformationByWord.word_id == self.id,
                                                           InformationByWord.information_id == information.id))
            logger.log(id=self.id, info=info)
            return
        inf_by_word = InformationByWord()
        inf_by_word.word = self
        inf_by_word.information = information
        db.add(inf_by_word)
        db.commit()