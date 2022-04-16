from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
# from wtforms import Fi
from wtforms.validators import DataRequired


class LikeCommentForm(FlaskForm):
    text = TextAreaField('Введите текст комментария', validators=[DataRequired()])
    submit = SubmitField('Отправить')
    submit1 = SubmitField('Нравится', id='submit1')