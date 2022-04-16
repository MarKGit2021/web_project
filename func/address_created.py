from random import randint


def address_created(object_id):
    """
    Метод, который генерирует адресс для страниц с информацией
    :param object_id: int
    :return: str
    """
    one = str(randint(100, 999))
    return one + str(object_id)


def get_id_for_address(folder):
    """
    Метод, который расшифровывает адресс страниц информации чтобы узнать id
    :param folder: str
    :return: int
    """
    return int(str(folder)[3:])