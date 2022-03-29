import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Information(SqlAlchemyBase):
    __tablename__ = 'information'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    folder = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    points = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    user = orm.relation("User", back_populates='information')
    comments = orm.relation('Comment', back_populates='information')

