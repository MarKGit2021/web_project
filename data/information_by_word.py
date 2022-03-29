import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


# Пока написала, пусть будет. Если что, можно вырезать
class InformationByWord(SqlAlchemyBase):
    __tablename__ = 'information_by_word'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    word_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('words.id'), nullable=False)
    information_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('information.id'), nullable=False)
    word = orm.relation('Word')
    information = orm.relation('Information')
