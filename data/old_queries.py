import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class OldQueries(SqlAlchemyBase):
    __tablename__ = 'old_queries'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    information_by_word_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('information_by_word.id'),
                                               nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    type_of_query = sqlalchemy.Column(sqlalchemy.String, nullable=False,
                                      default='r')  # По умолчанию, пользователь читает страницу
    user = orm.relation('User')
    # information_by_word = orm.relation('InformationByWord')
