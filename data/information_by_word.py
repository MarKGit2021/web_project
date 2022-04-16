import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


# Класс я вернула. Честно говоря устала разбираться,
# как работает промежуточная таблица как таблица без класса, если рабоотать с калссами, а не с запросами
class InformationByWord(SqlAlchemyBase):
    __tablename__ = 'information_by_word'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    word_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('words.id'), nullable=False)
    information_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('information.id'), nullable=False)
    information = orm.relation('Information')
    word = orm.relation('Word')

    def __str__(self):
        return f'Промежуточная сущность Информация по слову id: {self.id}, information_id: {self.information_id},' \
               f' word_id: {self.word_id}, word: {self.word.word}'

    def __repr__(self):
        return f'Информация_по_слову(id: {self.id}, information_id: {self.information_id},' \
               f' word_id: {self.word_id})'