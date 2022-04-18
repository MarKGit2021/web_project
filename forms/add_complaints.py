from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class AddComplaint(FlaskForm):
    text = TextAreaField('Жалоба:', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Добавить')
