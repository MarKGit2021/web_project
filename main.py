from flask import render_template, Flask, request
from flask_login import LoginManager
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session
from data.information import Information
from data.words import Word
from forms.add_complaints import AddComplaint
from func.address_created import *
from func.add_information import add_information
from func.add_complaint import new_complaint
from forms.search_form import SearchForm
from forms.add_form import AddForm
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
    print(word)
    if len(list(words)) == 0:
        return redirect(f'/search/{word}')
    information = words[0].all_information
    if len(information) == 0:
        return redirect(f'/search/{word}')
    elif len(information) == 1:
        return redirect(f'/information/{address_created(information[0].id)}')
    else:
        return all_information(information, db)


a = True


@app.route('/add-new', methods=['POST', 'GET'])
def add_new_information():
    """
    Метод, который обрабатывает добавление информации.
    Если пользователь не залогинен, то его перенаправляют на страницу логина
    Пользователь может вставить файл, а может написать текст так.
    В приоритете написанный текст - если он есть, то береться он, а не файл
    :return:
    """
    # if a:# пока нет логина
    #     return redirect('/login')
    form = AddForm()
    error = []
    flag = True
    text = ''
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.is_submitted():
                if form.text.data.strip() != '':
                    flag = False
                    text = form.text.data.strip()
                if flag:
                    f = request.files['file']
                    text = f.read().strip()
                    if str(text)[2:-1].strip() == '':
                        return render_template('add_information.html', form=form,
                                               errors=['Выберите файл или введите информацию!'])
                word = form.word.data
                words = form.words.data
                # user_id = current_user.id
                add_information(db=db_session.create_session(), word=word, user_id=1, words=words, text=text)
                print(word, 6)
                return redirect(f'/search/{word}')
    return render_template('add_information.html', form=form, errors=error)


@app.route('/add_complaint/<int:object_id>', methods=['GET', 'POST'])
def add_complaints(object_id):
    form = AddComplaint()
    print('tyt', form.is_submitted())
    if form.is_submitted():
        print('tyt1')
        text = form.text.data
        # user_id = current_user.id
        user_id = 1
        new_complaint(db=db_session.create_session(), text=text, object_id=object_id, user_id=user_id)
        return redirect('/')
    return render_template('add_complaints.html', form=form)


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
    print(word, 8)
    """
    Метод, который возвращает страницу с выбором
    :param word: str слово
    :return:
    """
    db = db_session.create_session()
    query = list(db.query(Word).filter(Word.word == word))
    if len(query) == 0 or len(query[0].all_information) == 0:
        return render_template('add_or_wiki_site.html', word=word, is_authenticated=False)
    else:
        print(word, 11)
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
    print(information_id)
    information = db.query(Information).filter(Information.id == information_id)
    if len(list(information)) == 0:
        abort(404)
    print(information[0].text)
    return render_template(information[0].text, **information[0].get_information(), site='/')


@app.route('/', methods=['GET', 'POST'])
def main_func():
    """
    Метод, который обрабатывает главную страницу + поле поиска
    :return: главная страница
    """
    form = SearchForm()
    if form.validate_on_submit():
        return search(form.word.data.strip().lower())
    db = db_session.create_session()
    top_information = get_top_information(db)
    return render_template('main.html', is_authenticated=False, form=form,
                           inf=top_information, len_form=len(top_information))


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.run(port=8080, host='127.0.0.1')
