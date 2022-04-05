from data.information import Information


def get_top_information(db):
    """
    Метод, который возвращает списки словарей с данными о самых популярных информациях
    :param db: База данных, с которой работаем
    :return: list[dict]
    """
    return [i.get_information() for i in sorted(db.query(Information).filter(), key=lambda x: x.points)]
