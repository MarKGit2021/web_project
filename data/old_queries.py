import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class OldQueries(SqlAlchemyBase):
    __tablename__ = 'old_queries'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    information_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('information.id'),
                                       nullable=False)
    word_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('words.id'), nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    type_of_query = sqlalchemy.Column(sqlalchemy.String, nullable=False,
                                      default='r')  # По умолчанию, пользователь читает страницу
    user = orm.relation('User')
    word = orm.relation('Word')
    information = orm.relation('Information')

    # information_by_word = orm.relation('InformationByWord')

    def get_old_queries_information(self):
        return {
            'modified_date': self.modified_date,
            'type_of_query': self.type_of_query,
            'word': self.word.word
            }
