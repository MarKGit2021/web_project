import flask
from flask import jsonify, request

from data.words import Word
from data.api_token import APIToken
from data import db_session
from func.add_information import add_information

blueprint = flask.Blueprint(
    'information_api',
    __name__,
    template_folder='templates'
    )


def search(word: str = None):
    db = db_session.create_session()
    word = db.query(Word).filter(Word.word == word)
    if len(list(word)) == 0:
        db.close()
        return []
    information = {i.information.points: i.information.get_information() for i in word.all_information}
    db.close()
    return information


@blueprint.route('/api/main_information/<word>', methods=['GET'])
def get_information(word):
    information = search(word)
    return jsonify(information[max(information.keys())])


@blueprint.route('/api/all_information/<word>', methods=['GET'])
def get_all_information(word):
    return jsonify(search(word))


@blueprint.route('/api/information', methods=['POST'])
def add_new_information():
    if not request.json:
        return jsonify({'error': 'Empty request'}), 400
    elif not all(key in request.json for key in
                 ['text', 'token', 'word', 'words']):
        return jsonify({'error': 'Bad request'}), 400
    db = db_session.create_session()
    try:
        user = db.query(APIToken).filter(APIToken.token ==
                                         request.json['token'])[0].user
    except TypeError:
        db.close()
        return jsonify({"status": "bad", 'error': 'Token is not valid'}), 401
    add_information(db, word=request.json['word'], user_id=user.id, words=request.json['words'], text=request.json['text'])
    db.commit()
    db.close()
    return jsonify({"status": "Ok"}), 200

