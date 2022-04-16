from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class ReadComplaint(FlaskForm):
    text = TextAreaField('Комментарии к жалобе:')
    submit = SubmitField('Добавить', id='add')
    submit1 = SubmitField('Решено', id='res')
    for_inf = SubmitField('К информации', id='inf')