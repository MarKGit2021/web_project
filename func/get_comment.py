from data.comments import Comment


def get_comment(db, information_id: int):
    """
    Метод, достающий из бд информауию о комментариях\n
    :param db: База данных, с которой работаем
    :param information_id: int
    :return:
    """
    comment = [i.get_comment_information()
               for i in db.query(Comment).filter(Comment.information_id == information_id)]
    db.close()
    return comment
