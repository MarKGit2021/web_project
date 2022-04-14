import flask
from flask import jsonify, request

from data.information import Information
from data.words import Word
from data.api_token import APIToken
from data import db_session
from func.add_information import add_information
from func.address_created import get_id_for_address

blueprint = flask.Blueprint(
    'information_api',
    __name__,
    template_folder='templates'
    )


def search(word: str):
    """
    Метод, который ищет всю информацию по слову
    :param word: str, слово для поиска
    :return:
    """
    db = db_session.create_session()
    word = db.query(Word).filter(Word.word == word)
    if len(list(word)) == 0:
        db.close()
        return []
    information = {i.information.points: i.information.get_information() for i in word[0].all_information}
    db.close()
    return information


@blueprint.route('/api/main_information/<word>', methods=['GET'])
def get_information(word):
    """
    Метод, который возвращает информацию о статье по заданному слову.
    :param word:
    :return:
    """
    information = search(word)
    return jsonify(information[max(information.keys())])


@blueprint.route('/api/all_information/<word>', methods=['GET'])
def get_all_information(word):
    """
    Возвращает все статьи по слову
    :param word:
    :return:
    """
    return jsonify(search(word))


@blueprint.route('/api/information', methods=['POST'])
def add_new_information():
    """
    Добавляет информацию только если есть токен
    :return:
    """
    if not request.json:
        return jsonify({"status": "Bad", 'error': 'Empty request'}), 400
    elif not all(key in request.json for key in
                 ['text', 'token', 'word', 'words']):
        return jsonify({"status": "Bad", 'error': 'Bad request'}), 400
    db = db_session.create_session()
    try:
        user = db.query(APIToken).filter(APIToken.token ==
                                         request.json['token'])
        user = list(user)[0].user
    except IndexError:
        db.close()
        return jsonify({"status": "Bad", 'error': 'Token is not valid'}), 401
    add_information(db, word=request.json['word'], user_id=user.id, words=request.json['words'],
                    text=request.json['text'])
    db.commit()
    db.close()
    return jsonify({"status": "Ok"}), 200


@blueprint.route('/api/information/<object_id>', methods=['DELETE'])
def blocking_information(object_id):
    """
    Блокирует информацию только если есть токен и пользователь администратор
    :param object_id:
    :return:
    """
    if 'token' not in request.json:
        return jsonify({'error': 'Empty request'}), 400
    if len(str(object_id)) < 4:
        return jsonify({"status": "Bad", 'error': 'Bad request'}), 400
    db = db_session.create_session()
    try:
        user = db.query(APIToken).filter(APIToken.token ==
                                         request.json['token'])[0].user
    except TypeError:
        db.close()
        return jsonify({"status": "Bad", 'error': 'Token is not valid'}), 401
    if user.type_of_user != 2:
        db.close()
        return jsonify({"status": "Bad", 'error': 'Access is denied'}), 403
    information_id = get_id_for_address(object_id)
    information = db.query(Information).filter(Information.id == information_id)
    if len(list(information)) == 0:
        db.close()
        return jsonify({"status": "Bad", "error": "Not Found"}), 404
    information = information[0]
    information.is_blocked = True
    db.commit()
    db.close()
    return jsonify({"status": "Ok"}), 200
