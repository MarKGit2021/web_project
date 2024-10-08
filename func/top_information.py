from data.information import Information


def get_top_information(db):
    """
    Метод, который возвращает списки словарей с данными о самых популярных информациях\n
    :param db: База данных, с которой работаем
    :return: list[dict]
    """
    return [i.get_information() for i in list(filter(lambda x: not x.is_blocked,
                                                     sorted(db.query(Information).all(),
                                                            key=lambda x: -x.points)))[:10]]
