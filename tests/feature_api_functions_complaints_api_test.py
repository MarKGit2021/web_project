from requests import get, post, put, delete

#  Берем все жалобы
print(get('http://127.0.0.1:8080/api/complaints', json={'token': '360:210118'}).json())

# Отмечаем жалобу прочитанной
print(put('http://127.0.0.1:8080/api/complaints/1', json={'token': '360:210118', 'is_reading': False}).json())
