from __future__ import annotations
from typing import TYPE_CHECKING

import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

if TYPE_CHECKING:
    from data.words import Word
from data.information_by_word import InformationByWord
from func.address_created import address_created


class Information(SqlAlchemyBase):
    __tablename__ = 'information'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    folder = sqlalchemy.Column(sqlalchemy.String)  # , nullable=False) - Пока информация сохраняется в файл,
    # нужно, чтобы в первый раз она сохранилась без пути
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    points = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    is_blocked = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    user = orm.relation("User", back_populates='information')
    comments = orm.relation('Comment', back_populates='information')
    all_words = orm.relation('InformationByWord', back_populates='information')

    def get_text_information(self) -> str:
        """
        Метод, который достает откуда-то содержимое информации. Пока достаю из файла.
        :return: str
        """
        if self.is_blocked:
            return 'Данная информация заблокирована оператором, тк она содержит нежелательный контент'
        with open(f"./templates/{self.folder[2:]}", 'r', encoding='utf-8') as file:
            text = file.read().strip()
        text = text.strip('{% extends "get_information.'
                          'html" %}').strip().strip('{% block content_1 %}').strip('{% endblock %}')
        return text

    def get_main_word(self):
        try:
            word = self.all_words[0].word.word
            return word
        except IndexError:
            self.is_blocked = True
            return
            # Надо будет сделать либо логирование, либо системные сообщения об ошибках администраторам

    def get_information(self):
        """
                Метод, который возвращает словарь, который можно легко вставить в html (render_template)
                :return: dict
        """
        return {'user_name': self.user.name, 'user_surname': self.user.surname,
                'modified_date': self.modified_date, 'points': self.points,
                'number_of_comments': len(self.comments),
                'main_word': self.get_main_word(),
                'error': self.is_blocked,
                'address': address_created(self.id), 'text': self.get_text_information()}

    def __str__(self):
        return f'Информация id: {self.id}; user_name: {self.user.name}; user_surname: {self.user.surname};' \
               f' date: {self.modified_date}; is_blocked: {self.is_blocked}; points: {self.points}'

    def __repr__(self):
        return f'Информация(id: {self.id}; user_id: {self.user_id}; date: {self.modified_date})'

    def save_text(self, text: str, folder: str = './templates/files/'):
        """
        Метод, который сохраняет текст в файл и сам записывает к нему путь.
        Если будем записываеть комменты в бд, то он будет как-то преобразовывть или еще что-то
        :param text: str, текст, который сохраняем
        :param folder: str, путь к папке, где будет лежать файл. По умолчанию стоит тот путь,
         который будет, если вызывать из main
        :return: None
        """
        if type(text) == bytes:
            # text = b'jhj'
            print(text)
            with open('prob.txt', 'wb') as file:
                file.write(text)
            with open('prob.txt', 'r', encoding='utf-8') as file:
                text = file.read().strip()
        if '<!DOCTYPE' in text:
            text = '>'.join(text.split('>')[1:]).strip()
        else:
            if text.strip()[0] != '<':
                text = f'<p>{text}</p>'
                text = text.replace('\n', '<br>')
        # text = text.replace('\r', '')
        text = text.replace('\\r', '')
        text = text.replace('\\n', '')
        text = text.replace('\\t', '')
        text = ''.join(''.join(text.strip('\\r')).split('\\n'))
        text = '''{% extends "get_information.html" %}
{% block content_1 %}
''' + text + '''
{% endblock %}
'''
        with open(f'{folder}information_{self.id}.html', 'w', encoding='utf-8') as file:
            file.write(text)
        self.folder = f'./files/information_{self.id}.html'

    def append_word(self, word: Word, db):
        """
        Метод, который добавляет к информации слово
        :param word: Word (слово, которое нужно добавить)
        :param db: база, с которой мы работаем
        :return: None
        """
        if len(list(db.query(InformationByWord).filter(InformationByWord.word_id == word.id,
                                                       InformationByWord.information_id == self.id))) != 0:
            return
        inf_by_word = InformationByWord()
        inf_by_word.word = word
        inf_by_word.information = self
        db.add(inf_by_word)
        db.commit()
