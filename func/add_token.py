from sqlalchemy import exc

from data.api_token import APIToken
from data import db_session


def add_token(db, user_id: int):
    # db = db_session.create_session()
    new_token = APIToken()
    new_token.user_id = user_id
    db.add(new_token)
    db.commit()
    new_token.generate_token()
    db.commit()
    return new_token
