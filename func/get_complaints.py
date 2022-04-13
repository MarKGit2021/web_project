from data import db_session
from data.complaints import Complaints


def get_complaints_information(db):
    res = [i.get_complaints_information() for i in db.query(Complaints).all()]
    res.sort(key=lambda x: not x['is_reading'])
    print(res)
    return res