import flask_login
from flask import render_template, Flask, request, flash
from flask_login import LoginManager, login_required, logout_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from data.users import LoginForm
from flask_login import login_user
from data import db_session
from data.api_token import APIToken
from data.complaints import Complaints
from data.information import Information
from data.users import User
from data.words import Word
from forms.like_comment import LikeCommentForm
from data.users import RegisterForm
from forms.add_complaints import AddComplaint
from forms.new_token import NewTokenForm
from forms.read_complaint import ReadComplaint
from func.add_comment import add_comment
from func.add_token import add_token
from func.address_created import *
from func.add_information import add_information
from func.add_complaint import new_complaint
from forms.search_form import SearchForm
from forms.add_form import AddForm
from func.get_comment import get_comment
from func.get_complaints import get_complaints_information
from func.get_likes import get_likes
from func.top_information import get_top_information

db_session.global_init('db/db.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def search(word: str):
    """
    Метод, который ищет информацию, и если находит в зависимости от количества перенаправляет на нужную страницу
    :param word: str, слово для поиска
    :return:
    """
    db = db_session.create_session()
    words = db.query(Word).filter(Word.word == word.strip())
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


@app.route('/add-new/<word>', methods=['POST', 'GET'])
def add_new_information(word):
    """
    Метод, который обрабатывает добавление информации.
    Если пользователь не залогинен, то его перенаправляют на страницу логина
    Пользователь может вставить файл, а может написать текст так.
    В приоритете написанный текст - если он есть, то береться он, а не файл
    :return:
    """
    if not flask_login.current_user.is_authenticated:# пока нет логина
        return redirect('/login')
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
                add_information(db=db_session.create_session(), word=word, user_id=flask_login.current_user.id,
                                words=words, text=text)
                return redirect(f'/search/{word.lower()}')
    return render_template('add_information.html', form=form, errors=error)


@app.route('/my-office', methods=["POST", "GET"])
def office():
    """
    Метод, который обрабатывает токины пользователя и показывает его личный кабинет
    :return:
    """
    db = db_session.create_session()
    current_user = flask_login.current_user
    if not current_user.is_authenticated:
        db.close()
        return redirect('/login')
    form = NewTokenForm()
    old_token = db.query(APIToken).filter(APIToken.is_blocked == False,
                                          APIToken.user_id == current_user.id)  # current_user.id)[0]
    if len(list(old_token)) == 0:
        old_token = add_token(db, current_user.id)
    else:
        old_token = old_token[0]
    if form.is_submitted():
        old_token.is_blocked = True
        db.commit()
        api_token = add_token(db, current_user.id)
        db.close()
        return redirect('/my-office')
    info = [i.get_information() for i in db.query(Information).filter(Information.user_id == current_user.id)]
    token = old_token.token
    user_information = current_user.get_user_information()
    db.close()
    return render_template('private_office.html', **user_information,
                           token=token, form=form, inf=info)


@app.route('/add_complaint/<int:object_id>', methods=['GET', 'POST'])
def add_complaints(object_id):
    """
    Метод, который обрабатывает добавление жалобы на определенную информацию
    :param object_id: int - зашифрованное id
    :return:
    """
    if not flask_login.current_user.is_authenticated:
        return redirect('/login')
    form = AddComplaint()
    if form.is_submitted():
        text = form.text.data
        user_id = flask_login.current_user.id
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
    """
    Метод, который возвращает страницу с выбором
    :param word: str слово
    :return:
    """
    db = db_session.create_session()
    query = list(db.query(Word).filter(Word.word == word))
    if len(query) == 0 or len(query[0].all_information) == 0:
        db.close()
        return render_template('add_or_wiki_site.html', word=word,
                               is_authenticated=flask_login.current_user.is_authenticated)
    else:
        db.close()
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
    information = db.query(Information).filter(Information.id == information_id)
    current_user = flask_login.current_user
    if len(list(information)) == 0:
        db.close()
        abort(404)
    else:
        information = information[0]
    form = LikeCommentForm()
    is_liked = False
    if current_user.is_authenticated:
        is_liked = current_user.check_like(db=db, information_id=information_id)
    likes = get_likes(db, information_id=information_id)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(f'/information/{folder}')
        if form.submit1.data:
            # add_like(db, user_id=current_user.id, information=information[0])
            flag = current_user.click_like(information=information, db=db)
            print(current_user.points, information.points)
            information.points += flag
            print(information.points)
            db.commit()
        if form.submit.data:
            text = form.text.data
            add_comment(db, user_id=current_user.id, information_id=information_id, text=text)
        db.close()
        return redirect(f'/information/{folder}')
    inf = information.get_information()
    type_of_user = 0
    if current_user.is_authenticated:
        type_of_user = current_user.type_of_user
    db.close()
    return render_template(information.folder, **inf, site='/', site1='/',
                           is_authenticated=True, name1=form, current_user=current_user, likes=likes, is_liked=is_liked,
                           comment=get_comment(db_session.create_session(), information_id),
                           type_of_user=type_of_user, folder=folder)


@app.route('/complaints')
def get_all_complaints():
    current_user = flask_login.current_user
    if not current_user.is_authenticated:
        return redirect('/login')
    db = db_session.create_session()
    if current_user.type_of_user != 2:
        db.close()
        abort(404)
    complaints_information = get_complaints_information(db)
    db.close()
    return render_template('all_complaints.html', complaints=complaints_information)


@app.route('/complaint/<object_id>', methods=['POST', 'GET'])
def get_complaint(object_id):
    """
    Метод, который отвечает за показ и обработку жалоб на информации (только для админов)
    :param object_id: id жалобы (не вижу смысла шифровать, тк это только админам
    :return:
    """
    form = ReadComplaint()
    db = db_session.create_session()
    current_user = flask_login.current_user
    if current_user.type_of_user != 2:
        db.close()
        abort(404)
    complaint = db.query(Complaints).filter(Complaints.id == object_id)[0]
    if form.is_submitted():
        print(form.for_inf.data)
        if form.submit.data:
            if form.text.data.strip() != '':
                complaint.text += f'''\n\n\tКомментарий администратора {current_user.name} {current_user.surname}\n''' \
                                  + form.text.data
                db.commit()
        if form.submit1.data:
            complaint.is_reading = True
            db.commit()
        if form.for_inf.data:
            folder = address_created(complaint.information.id)
            db.close()
            return redirect(f"/information/{folder}")
        db.close()
        return redirect(f'/complaint/{object_id}')
    name = complaint.user.name
    surname = complaint.user.surname
    db.close()
    return render_template('get_complaint.html', user_name=name, user_surname=surname, complaint=complaint, form=form)


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
    return render_template('main.html', is_authenticated=flask_login.current_user.is_authenticated, form=form,
                           inf=top_information, len_form=len(top_information))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data
            )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.run(port=8080, host='127.0.0.1')
