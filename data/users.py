import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    points = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    type_of_user = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    information = orm.relation("Information", back_populates='user')
    comments = orm.relation("Comment", back_populates='user')

    def check_password(self, password) -> bool:
        return self.hashed_password == password

    def get_user_information(self) -> dict:
        """
        Метод, который возвращает словарь, который можно легко вставить в html (render_template)
        :return: dct
        """
        return {
            'name': self.name,
            'surname': self.surname,
            'points': self.points,
            'modified_date': self.modified_date,
            'type': self.type_of_user
            }

    def __str__(self):
        return f'Пользователь с id: {self.id}; name: {self.name}; ' \
               f'surname: {self.surname}; email: {self.email}; ' \
               f'hashed password: {self.hashed_password}'

    def __repr__(self):
        return f'Пользователь с id: {self.id}'
