import flask
from flask import jsonify

from data.words import Word
from ..data import db_session
from ..data.information import Information

blueprint = flask.Blueprint(
    'information_api',
    __name__,
    template_folder='templates'
)

def search(word: str=None):
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

@blueprint.route('/api/all_information/<word>', methods=['GET']):
def get_all_information(word):
    return jsonify(search(word))