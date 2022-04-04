import datetime

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from likes import Like

from .db_session import SqlAlchemyBase

POINTS_CONST = 5  # Сколько нужно лайков, чтобы стать модератором


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    points = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False, index=True)
    __hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    type_of_user = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    information = orm.relation("Information", back_populates='user')
    comments = orm.relation("Comment", back_populates='user')
    queries = orm.relation('OldQueries', back_populates='user')

    def check_password(self, password) -> bool:
        return self.__hashed_password == password

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
               f'surname: {self.surname}; email: {self.email}'

    def __repr__(self):
        return f'Пользователь(id: {self.id})'

    def click_like(self, information_id, db):
        """
        Метод, который можно вызвать при нажатии пользователем на лайк:
        если лайк уже был нажат, то он удаляется. Если его не было, он создается
        :param information_id: int
        :param db: база, с которой работаем
        :return: bool - закрашивать лайк или нет.
        """
        if self.check_like(information_id, db):
            db.delete(db.query(Like).filter(Like.information_id == information_id,
                                            Like.user_id == self.id))
            db.commit()
            return False
        like = Like()
        like.user_id = self.id
        like.information_id = information_id
        db.add(Like)
        db.commit()
        return True

    def check_like(self, information_id, db):
        """
        Метод, который проверяет, ставил ли пользователь лайк на эту страничку
        :param information_id: int
        :param db: база, с которой работаем
        :return: bool, закрашивать лайк или нет
        """
        return len(db.query(Like).filter(Like.information_id == information_id,
                                         Like.user_id == self.id)) == 0

    def new_point(self):
        """
        Метод, который увеличивает количество лайков и проверяет, когда нужно повысить уровень пользователя
        :return: None
        """
        self.points += 1
        if self.points == POINTS_CONST:
            self.type_of_user = 1
