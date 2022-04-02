import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


# Этот класс в принципе тоже можно будет вырезать.
# Он нужен для того, чтобы в случае многоразового использования слова использовать меньще памяти
class Word(SqlAlchemyBase):
    __tablename__ = 'words'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    word = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    all_information = orm.relation("InformationByWord", back_populates='word')

    def __str__(self):
        return f"Слово id: {self.id}, word: {self.word}"

    def __repr__(self):
        return f'Слово(id: {self.id})'
