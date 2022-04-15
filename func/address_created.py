from random import randint


def address_created(object_id):
    """
    Метод, который генерирует адресс для страниц с информацией\n
    :param object_id: int
    :return: str
    """
    one = randint(100, 999)
    return str(object_id) + str(one)  # такой вариант оказался удобнее для декодировки


def get_id_for_address(folder):
    """
    Метод, который расшифровывает адресс страниц информации чтобы узнать id\n
    :param folder: str
    :return: int
    """
    return int(folder) // 1000  # 12345123 // 1000 = 12345
