from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class New_EntForm(FlaskForm):
    ent = StringField('Развлечение', validators=[DataRequired()])
    ent_type = SelectField('Категория', choices=[("kino", "Кино"), ("music", "Музыка"), ("game", "Игры")])
    content = TextAreaField('Описание', validators=[DataRequired()])

    submit = SubmitField('Принять')