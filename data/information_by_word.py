import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


# Этот класс я убрала. Таблица есть, класса нет,тк нам к нему обращаться не надо.
# Таблица нужна только как промежуточная сущность для связи вногие ко многим
class InformationByWord(SqlAlchemyBase):
    __tablename__ = 'information_by_word'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    word_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('words.id'), nullable=False)
    information_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('information.id'), nullable=False)
    information = orm.relation('Information')
