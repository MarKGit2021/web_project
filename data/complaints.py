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
    folder = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    information = orm.relation('Information')
    user = orm.relation('User')

    def get_complaints_text(self):
        """
                Метод, который достает откуда-то текст комментария. Пока текст достается из файла по пути folder
                :return: пока str
        """
        with open(self.folder, 'r', encoding='utf-8') as file:
            text = file.read().strip()
        return text

    def get_complaints_information(self):
        """
                Метод, который возвращает словарь, который можно легко вставить в html (render_template)
                :return: dict
        """
        return {
            'text': self.get_complaints_text(),
            'user_name': self.user.name,
            'user_surname': self.user.surname
            }

    def __str__(self):
        return f'Жалоба id: {self.id}, user_id: {self.user_id}, user_name: {self.user.name}, ' \
               f'user_surname: {self.user.surname}, information_id: {self.information_id}'

    def __repr__(self):
        return f'Жалоба(id: {self.id}, user_id: {self.user_id}, information_id: {self.information_id})'
