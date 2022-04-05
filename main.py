from flask import render_template, Flask
from flask_login import LoginManager

from data import db_session
from forms.search_form import SearchForm
from func.top_information import get_top_information

db_session.global_init('db/db.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# login_manager = LoginManager()
# login_manager.init_app(app)

def search(word):
    pass


@app.route('/')
def main_func():
    form = SearchForm()
    if form.validate_on_submit():
        print('tytyt')
        search(form.word)
    db = db_session.create_session()
    top_information = get_top_information(db)
    return render_template('main.html', is_authenticated=False, form=form,
                           inf=top_information, len_form=len(top_information))


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.run(port=8080, host='127.0.0.1')
