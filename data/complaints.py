import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Complaints(SqlAlchemyBase):
    __tablename__ = 'complaints'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    information_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('information.id'), nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_reading = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    information = orm.relation('Information')
    user = orm.relation('User')

    def get_complaints_text(self):
        """
                Метод, который достает откуда-то текст комментария. Я решила, что жалобы можно хранить в бд
                :return: пока str
        """
        return self.text

    def get_complaints_information(self):
        """
                Метод, который возвращает словарь, который можно легко вставить в html (render_template)
                :return: dict
        """
        return {
            'text': self.get_complaints_text(),
            'user_name': self.user.name,
            'user_surname': self.user.surname,
            'modified_date': self.modified_date,
            'is_reading': self.is_reading,
            'main_word': self.information.get_main_word(),
            'id': self.id
            }

    def __str__(self):
        return f'Жалоба id: {self.id}, user_id: {self.user_id}, user_name: {self.user.name}, ' \
               f'user_surname: {self.user.surname}, information_id: {self.information_id}'

    def __repr__(self):
        return f'Жалоба(id: {self.id}, user_id: {self.user_id}, information_id: {self.information_id})'
