import datetime
import random

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class APIToken(SqlAlchemyBase):
    __tablename__ = 'api_token'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    token = sqlalchemy.Column(sqlalchemy.String, unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    is_blocked = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user = orm.relation("User")

    def __str__(self):
        return f'API-токет id: {self.id}, user_email: {self.user.email}, ' \
               f'user_id: {self.user_id}, is_blocked: {self.is_blocked}, token: {self.token}'

    def __repr__(self):
        return f'Api-токен(id={self.id}, token={self.token})'

    def get_information(self):
        return {
            'token': self.token,
            'is_blocked': self.is_blocked
            }

    def generate_token(self):
        self.token = f"{random.randint(100, 999)}:{random.randint(1000, 9999)}{self.id}"
