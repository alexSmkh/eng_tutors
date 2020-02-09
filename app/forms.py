from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class MessageForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    phone = StringField('Ваш телефон', validators=[DataRequired()])
    message = StringField('Сообщение', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Отправить')


class BookingForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    phone = StringField('Ваш телефон', validators=[DataRequired()])
    submit = SubmitField('Записаться на пробное занятие', validators=[DataRequired()])


class TeacherSelectionForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    phone = StringField('Ваш телефон', validators=[DataRequired()])
    submit = SubmitField('Найти мне преподавателя')
    goals = RadioField(
        'Какая цель занятий?',
        choices=[
            ('travel', 'Для путешествий'),
            ('study', 'Для школы'),
            ('work', 'Для работы'),
            ('relocate', 'Для переезда')
        ],
        validators=[DataRequired()]     
    )
    time = RadioField(
        'Сколько времени есть?',
        choices=[
            ('1-2', '1-2 часа в неделю'),
            ('3-5', '3-5 часов в неделю'),
            ('5-7', '5-7 часов в неделю'),
            ('7-10', '7-10 часов в неделю')
        ],
        validators=[DataRequired()]     
    )


