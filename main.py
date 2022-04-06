from flask import render_template, Flask
from flask_login import LoginManager
from werkzeug.utils import redirect

from data import db_session
from data.information import Information
from forms.search_form import SearchForm
from func.top_information import get_top_information

db_session.global_init('db/db.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# login_manager = LoginManager()
# login_manager.init_app(app)

def search(word):
    pass


@app.route('/search/<int:folder>', methods=['GET'])
def search_information(folder):
    pass


@app.route('/information/<int:folder>', methods=['GET'])
def get_information(folder):
    information_id = int(str(folder)[3:])
    db = db_session.create_session()
    information = db.query(Information).filter(Information.id == information_id)
    if len(list(information)) == 0:
        return redirect('/')
    # print(information[0].get_text_information(), type(information[0]))
    return render_template(information[0].folder, **information[0].get_information(), site='/')


@app.route('/')
def main_func():
    form = SearchForm()
    if form.validate_on_submit():
        search(form.word)
    db = db_session.create_session()
    top_information = get_top_information(db)
    return render_template('main.html', is_authenticated=False, form=form,
                           inf=top_information, len_form=len(top_information))


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.run(port=8080, host='127.0.0.1')
