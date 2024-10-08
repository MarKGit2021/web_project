from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class UpdateForm(FlaskForm):
    """
    Форма для изменения информации
    """
    text = TextAreaField('Информация', validators=[DataRequired()])
    submit = SubmitField('Править')
