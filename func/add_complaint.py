from data.complaints import Complaints
# from data import db_session
from func.address_created import get_id_for_address


def new_complaint(db, text: str, object_id: int, user_id: int):
    """
    Метод, который создает и сохраняет жалобу
    :param db: база данных
    :param text: str - текст жалобы
    :param object_id: int - id информации, на которую жалуются
    :param user_id: int - id пользователя, который пожаловался
    :return:
    """
    # db = db_session.create_session()
    new_comp = Complaints()
    new_comp.information_id = get_id_for_address(object_id)
    new_comp.user_id = user_id
    new_comp.text = text
    db.add(new_comp)
    db.commit()
    db.close()
    return True