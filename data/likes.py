import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Like(SqlAlchemyBase):
    """
    Класс, который сохраняет, кому пользователь уже ставил лайк
    """
    __tablename__ = 'likes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    information_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('information.id'), nullable=False)

    def __str__(self):
        return f'Лайки id: {self.id}, information_id: {self.information_id}, user_id: {self.user_id}'

    def __repr__(self):
        return f'Лайки(id: {self.id})'