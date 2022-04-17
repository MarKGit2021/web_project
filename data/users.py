import datetime

import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired
from .likes import Like

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
    tokens = orm.relation('APIToken', back_populates='user')

    def set_password(self, password):
        self.__hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__hashed_password, password)

    def get_user_information(self) -> dict:
        """
        Метод, который возвращает словарь, который можно легко вставить в html (render_template)
        :return: dct
        """
        return {
            'name': self.name,
            'surname': self.surname,
            'points': self.points,
            'user_email': self.email,
            'modified_date': self.modified_date,
            'type': self.type_of_user
            }

    def __str__(self):
        return f'Пользователь с id: {self.id}; name: {self.name}; ' \
               f'surname: {self.surname}; email: {self.email}'

    def __repr__(self):
        return f'Пользователь(id: {self.id})'

    def click_like(self, information, db) -> int:
        """
        Метод, который можно вызвать при нажатии пользователем на лайк:
        если лайк уже был нажат, то он удаляется. Если его не было, он создается
        :param information: information
        :param db: база, с которой работаем
        :return: bool - закрашивать лайк или нет.
        """
        if information.user_id == self.id:
            return 0
        if self.check_like(information.id, db):
            db.delete(db.query(Like).filter(Like.information_id == information.id,
                                            Like.user_id == self.id)[0])
            information.user.new_point(-1)
            db.commit()
            return -1
        like = Like()
        like.user_id = self.id
        like.information_id = information.id
        information.user.new_point()
        db.add(like)
        db.commit()
        return 1

    def check_like(self, information_id: int, db):
        """
        Метод, который проверяет, ставил ли пользователь лайк на эту страничку
        :param information_id: int
        :param db: база, с которой работаем
        :return: bool, закрашивать лайк или нет
        """
        return len(list(db.query(Like).filter(Like.information_id == information_id,
                                              Like.user_id == self.id))) != 0

    def new_point(self, value: int = 1):
        """
        Метод, который увеличивает количество лайков и проверяет, когда нужно повысить уровень пользователя
        :return: None
        """
        self.points += value
        if self.points >= POINTS_CONST:
            self.type_of_user = 1
        else:
            self.type_of_user = 0
