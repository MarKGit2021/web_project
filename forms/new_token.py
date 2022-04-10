from flask_wtf import FlaskForm
from wtforms import SubmitField


class NewTokenForm(FlaskForm):
    submit = SubmitField('Новый токен')
