import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    folder = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    information_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('information.id'), nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    is_blocked = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    information = orm.relation("Information")
    user = orm.relation('User')

    def blocked(self, flag=True):
        self.is_blocked = flag

    def get_text(self):
        """
        Метод, который достает откуда-то текст комментария. Пока текст достается из файла по пути folder
        :return: пока str
        """
        print(self.folder)
        with open(self.folder, 'r', encoding='utf-8') as file:
            text = file.read().strip()
        return text

    def get_comment_information(self) -> dict:
        """
        Метод, который возвращает словарь, который можно легко вставить в html (render_template)
        :return: dict
        """
        dct = {'user_name': self.user.name,
               'user_surname': self.user.surname,
               'modified_date': self.modified_date,
               'error': self.is_blocked}
        if self.is_blocked:  # Если комментарий заблокирован, то текст комментария заменяется
            # на сообщение о блокировке, а html сообщается об ошибке, чтобы как-то его поменять
            # (или не менять, как успеем)
            dct['text'] = 'Данный комментарий заблокирован оператором из-за наличия в нем нежелательного контента'
        else:
            dct['text'] = self.get_text()
        return dct

    def __str__(self):
        return f'Комментарий с id: {self.id}; user_id: {self.user_id}; user_name: {self.user.name}; ' \
               f'user_surname: {self.user.surname}; information_id: {self.information_id};' \
               f' date: {self.modified_date}; is_blocked: {self.is_blocked}'

    def __repr__(self):
        return f'Комментарий id: {self.id}; user_id: {self.user_id}; date: {self.modified_date}'
