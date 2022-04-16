from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    word = StringField('Введите основное слово', validators=[DataRequired()])
    words = StringField('Введите основные слова для поиска (формат: слово; слово)')
    submit = SubmitField('Добавить')
    text = TextAreaField('Введите информацию')