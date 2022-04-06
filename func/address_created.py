from random import randint


def address_created(object_id):
    one = str(randint(100, 999))
    return one + str(object_id)


def get_id_for_address(folder):
    return int(str(folder)[3:])
