from data.complaints import Complaints


def get_complaints_information(db):
    """
    Метод, который выдает отсортированную информацию о жалобах\n
    :param db: База данных, с которой работаем
    :return: list
    """
    res = [i.get_complaints_information() for i in db.query(Complaints).all()]
    res.sort(key=lambda x: x['is_reading'])
    return res
