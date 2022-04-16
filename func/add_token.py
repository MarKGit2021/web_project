from data.api_token import APIToken


def add_token(db, user_id: int):
    """
    Метод, который содает и сохраняет новый токен
    :param db: db
    :param user_id: int
    :return:
    """
    new_token = APIToken()
    new_token.user_id = user_id
    db.add(new_token)
    db.commit()
    new_token.generate_token()
    db.commit()
    return new_token