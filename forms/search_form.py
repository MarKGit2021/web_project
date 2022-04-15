from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    word = StringField('Введите слово', validators=[DataRequired()])
    submit = SubmitField('Искать')
