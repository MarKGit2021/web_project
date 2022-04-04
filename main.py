from flask import render_template, Flask
from flask_login import LoginManager

from data import db_session

db_session.global_init('db/db.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route('/')
def main_func():
    return render_template('headline.html', is_authenticated=False)


if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.run(port=8080, host='127.0.0.1')
