from flask import render_template, Flask, request, flash
from flask_login import LoginManager
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session
from data.api_token import APIToken
from data.information import Information
from data.users import User
from data.words import Word
from forms.like_comment import LikeCommentForm
from forms.add_complaints import AddComplaint
from forms.new_token import NewTokenForm
from func.add_comment import add_comment
from func.add_like import add_like
from func.add_token import add_token
from func.address_created import *
from func.add_information import add_information
from func.add_complaint import new_complaint
from forms.search_form import SearchForm
from forms.add_form import AddForm
from func.get_comment import get_comment
from func.get_likes import get_likes
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
    db.close()
    if len(list(words)) == 0:
        return redirect(f'/search/{word}')
    information = words[0].all_information
    if len(information) == 0:
        return redirect(f'/search/{word}')
    elif len(information) == 1:
        return redirect(f'/information/{address_created(information[0].information_id)}')
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
                return redirect(f'/search/{word.lower()}')
    return render_template('add_information.html', form=form, errors=error)


@app.route('/my-office', methods=["POST", "GET"])
def office():
    """
    Метод, который обрабатывает токины пользователя и показывает его личный кабинет
    :return:
    """
    # if not current_user.is_authenticated:
    #     return redirect('/login')
    db = db_session.create_session()
    current_user = db.query(User).first()
    form = NewTokenForm()
    old_token = db.query(APIToken).filter(APIToken.is_blocked == False, APIToken.user_id == 1)  # current_user.id)[0]
    if len(list(old_token)) == 0:
        print(*db.query(APIToken).all())
        old_token = add_token(db, current_user.id)
    else:
        old_token = old_token[0]
    print(form.is_submitted())
    if form.is_submitted():
        old_token.is_blocked = True
        db.commit()
        api_token = add_token(db, current_user.id)
        print('tyt')
        db.close()
        return redirect('/my-office')
    db.close()
    return render_template('private_office.html', **current_user.get_user_information(),
                           token=old_token.token, form=form)


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
    db.close()
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
        db.close()
        return render_template('add_or_wiki_site.html', word=word, is_authenticated=False)
    else:
        db.close()
        print(word, 11)
        return search(word)


@app.route('/information/<int:folder>', methods=['GET', 'POST', 'PUT'])
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
    current_user = db.query(User).first()
    if len(list(information)) == 0:
        db.close()
        abort(404)
    print(information[0])
    form = LikeCommentForm()
    likes, is_liked = get_likes(db, information_id=information_id, user_id=current_user.id)
    if request.method == 'POST':
        if form.submit1.data and not is_liked:
            add_like(db, user_id=current_user.id, information=information[0])
        if form.submit.data:
            text = form.text.data
            print(text)
            add_comment(db, user_id=current_user.id, information_id=information_id, text=text)
        db.close()
        return redirect(f'/information/{folder}')
    db.close()
    print(is_liked, 'is_liked')
    return render_template(information[0].folder, **information[0].get_information(), site='/', site1='/',
                           is_authenticated=True, name1=form, current_user=current_user, likes=likes, is_liked=is_liked,
                           comment=get_comment(db_session.create_session(), information_id))


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
    db.close()
    return render_template('main.html', is_authenticated=False, form=form,
                           inf=top_information, len_form=len(top_information))


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.run(port=8080, host='127.0.0.1')
