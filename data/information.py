import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'information_by_word',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('words', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('words.id')),
    sqlalchemy.Column('information', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('information.id')),
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True)
    )


class Information(SqlAlchemyBase):
    __tablename__ = 'information'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    folder = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    points = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    is_blocked = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    user = orm.relation("User", back_populates='information')
    comments = orm.relation('Comment', back_populates='information')

    def get_text_information(self) -> str:
        """
        Метод, который достает откуда-то содержимое информации. Пока достаю из файла.
        :return: str
        """
        pass

    def get_information(self):
        """
                Метод, который возвращает словарь, который можно легко вставить в html (render_template)
                :return: dict
        """
        dct = {
            'user_name': self.user.name,
            'user_surname': self.user.surname,
            'error': self.is_blocked,
            'modified_date': self.modified_date,
            'points': self.points,
            'number_of_comments': len(self.comments)
            }
        if self.is_blocked:
            dct['text'] = 'Данная информация заблокирована оператором, тк она содержит нежелательный контент'
        else:
            dct['text'] = self.get_text_information()
        return dct

    def __str__(self):
        return f'Информация id: {self.id}; user_name: {self.user.name}; user_surname: {self.user.surname};' \
               f' date: {self.modified_date}; is_blocked: {self.is_blocked}; points: {self.points}'

    def __repr__(self):
        return f'Информация id: {self.id}; user_id: {self.user_id}; date: {self.modified_date}'


