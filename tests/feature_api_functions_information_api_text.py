from requests import get, post, put, delete

#  Берем основную информацию по слову
print(get('http://127.0.0.1:8080/api/main_information/физика').json())

# Берем всю информацию по слову
print(get('http://127.0.0.1:8080/api/all_information/физика').json())
# Добавляем информацию
print(post('http://127.0.0.1:8080/api/information', json={"text": 'text', "token": '929:540117',
                                                          "word": 'new_word', "words": None}).json())
