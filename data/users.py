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
    comment = orm.relation("Comment", back_populates='user')

    def check_password(self, password):
        return self.hashed_password == password
