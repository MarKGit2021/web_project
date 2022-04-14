import flask
from flask import jsonify, request

from data.complaints import Complaints
from data.api_token import APIToken
from data import db_session

blueprint = flask.Blueprint(
    'complaints_api',
    __name__,
    template_folder='templates'
    )


def check_status(dct: dict, db, number: int = 2):
    if not dct:
        return jsonify({"status": "Bad", 'error': 'Empty request'}), 400, False
    if 'token' not in dct:
        return jsonify({"status": "Bad", 'error': 'Bad request'}), 400, False
    token = db.query(APIToken).filter(APIToken.token == dct['token'])
    if len(list(token)) == 0:
        return jsonify({"status": "Bad", 'error': 'Token is not valid'}), 401, False
    if token[0].user.type_of_user < number:
        return jsonify({"status": "Bad", 'error': 'Access is denied'}), 403, False
    return {}, 200, True


@blueprint.route('/api/complaints', methods=['GET'])
def get_all():
    db = db_session.create_session()
    check = check_status(db=db, dct=request.json)
    print(check)
    if not check[-1]:
        return check[0], check[1]
    complaints = {i.id: i.get_complaints_information() for i in db.query(Complaints).all()}
    db.close()
    return jsonify(complaints), 200


@blueprint.route('/api/complaints/<object_id>', methods=['PUT'])
def set_status(object_id):
    db = db_session.create_session()
    check = check_status(db=db, dct=request.json)
    if not check[-1]:
        db.close()
        return check[0], check[1]
    if 'is_reading' not in request.json:
        db.close()
        return jsonify({"status": "Bad", 'error': 'Bad request'}), 400
    complaint = db.query(Complaints).filter(Complaints.id == object_id)
    if len(list(complaint)) == 0:
        db.close()
        return jsonify({"status": "Bad", "error": "Not Found"}), 404
    complaint = complaint[0]
    complaint.is_reading = request.json['is_reading']
    db.commit()
    db.close()
    return jsonify({'status': 'Ok'}), 200
