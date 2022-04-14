import data.information
import data.db_session
import os


data.db_session.global_init('../db/db.db')
db = data.db_session.create_session()
os.chdir("..")
info = data.information.Information()
info.id = 228
info.is_blocked = False
print(info.is_blocked)
print(info.get_main_word())
print(info.is_blocked)
