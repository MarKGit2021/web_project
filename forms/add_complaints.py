from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddComplaint(FlaskForm):
    text = TextAreaField('Жалоба:', validators=[DataRequired()])
    submit = SubmitField('Добавить')
