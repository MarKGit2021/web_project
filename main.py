from flask import render_template, Flask
from flask_login import LoginManager
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session
from data.information import Information
from data.words import Word
from func.address_created import *
from forms.search_form import SearchForm
from func.top_information import get_top_information

db_session.global_init('db/db.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# login_manager = LoginManager()
# login_manager.init_app(app)

def search(word: str):
    """
    Метод, который ищет информацию, и если находит в зависимости от количества перенаправляет на нужную страницу
    :param word: str, слово для поиска
    :return:
    """
    db = db_session.create_session()
    words = db.query(Word).filter(Word.word == word.strip())
    if len(list(words)) == 0:
        return redirect(f'/search/{word}')
    information = words[0].all_information
    if len(information) == 0:
        return redirect(f'/search/{word}')
    elif len(information) == 1:
        return redirect(f'/information/{address_created(information[0].id)}')
    else:
        return all_information(information, db)


# def add_new_information():
#         new_word = Word()
#         new_word.word = word.strip()
#         db.add(new_word)
#         db.commit()

def all_information(information, db):
    """
    Метод, который выводит несколько 'ссылок' на информацию
    :param information: list список information_by_word
    :param db: db
    :return: страницу с несколькими ссылками
    """
    inf_information = list(map(lambda x: db.query(Information).filter(Information.id
                                                                      == x.information_id
                                                                      )[0].get_information(),
                               information))
    print(inf_information)
    return render_template('all_information.html', inf_information=inf_information)


@app.route('/search/<word>', methods=['GET'])
def search_information(word):
    """
    Метод, который возвращает страницу с выбором
    :param word:
    :return:
    """
    db = db_session.create_session()
    query = list(db.query(Word).filter(Word.word == word))
    if len(query) == 0 or len(query[0].all_information) == 0:
        return render_template('add_or_wiki_site.html', word=word)
    else:
        return search(word)


@app.route('/information/<int:folder>', methods=['GET'])
def get_information(folder):
    """
    Метод, который выводит информацию пользователя. Адрес записывается как три рандомные цыфры + айди информации
    Если такой информации нет, он перенаправляет на страницу поиска (которой пока нет, поэтому на главную)
    :param folder: int число типа: xxxid
    :return: страницу html
    """
    information_id = get_id_for_address(folder)
    db = db_session.create_session()
    information = db.query(Information).filter(Information.id == information_id)
    if len(list(information)) == 0:
        abort(404)
    return render_template(information[0].folder, **information[0].get_information(), site='/')


@app.route('/', methods=['GET', 'POST'])
def main_func():
    form = SearchForm()
    if form.validate_on_submit():
        print('tytyt')
        return search(form.word.data)
    db = db_session.create_session()
    top_information = get_top_information(db)
    return render_template('main.html', is_authenticated=False, form=form,
                           inf=top_information, len_form=len(top_information))


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.run(port=8080, host='127.0.0.1')
