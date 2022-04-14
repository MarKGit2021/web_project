import data.information
import data.db_session


data.db_session.global_init('db/db.db')
db = data.db_session.create_session()
info = data.information.Information()
info.id = 228
info.is_blocked = False
print(info.is_blocked)
print(info.get_main_word())
print(info.is_blocked)
print(info.get_main_word())
print(info.get_main_word())
print(info.get_main_word())
