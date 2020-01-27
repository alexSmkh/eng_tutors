import json

from flask import render_template, abort, request, url_for, redirect, flash

from app import app, db 
from app.models import Teacher, Goal, Request, Booking
from app.forms import BookingForm, TeacherSelectionForm, MessageForm
from tools import update_data_in_file
from global_variables import TEACHERS, GOALS, EMOJI, RU_DAYS_SHORT, RU_DAYS



@app.route('/')
def main():
    teachers = db.session.query(Teacher).order_by(Teacher.rating.desc())
    goals = db.session.query(Goal).all()
    context = {
        'teachers': teachers,
        'goals': goals,
        'emoji': EMOJI
    }
    return render_template('index.html', **context)


@app.route('/goals/<goal_slug>')
def goal(goal_slug):
    goal = db.session.query(Goal).filter(Goal.slug == goal_slug).first()
    teachers = db.session.query(Teacher)\
    .filter(Teacher.goals.contains(goal))\
    .order_by(Teacher.rating.desc())

    if not teachers: 
        abort(404)

    context = {
        'teachers': teachers,
        'emoji': EMOJI[goal_slug],
        'goal': goal
    }
    return render_template('goal.html', **context)


@app.route('/profiles/<int:teacher_id>')
def profile(teacher_id):
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    schedule = json.loads(teacher.schedule)
    context = {
        'teacher': teacher,
        'ru_days': RU_DAYS_SHORT,
        'schedule': json.loads(teacher.schedule)
    }
    return render_template('profile.html', **context)


@app.route('/sent', methods=['GET','POST'])
def sent():
    context = json.loads(request.args.get('context'))
    return render_template('sent.html', **context)


@app.route('/booking/<string:teacher_id>', methods=['GET', 'POST'])
def booking(teacher_id):
    teacher = TEACHERS.get(teacher_id)
    if not teacher:
        abort(404)

    form = BookingForm()
    if form.validate_on_submit():
        update_data_in_file(
            'bookings',
            {'name': form.name.data,
             'phone': form.phone.data,
             'day': request.args.get('day'),
             'time': request.args.get('time')}
        ) 

        weekday_ru = request.args.get('day')
        time = request.args.get('time')
        weekday_en = next(
            (day_en for day_en, day_ru in RU_DAYS.items() if weekday_ru == day_ru),
            None
        )
        TEACHERS[teacher_id]['free'][weekday_en][time] = False

        context = {
            'name': form.name.data,
            'phone': form.phone.data,
            'lesson_day':  weekday_ru,
            'lesson_time': time,
            'subject': 'trial',
            'subject_description': 'Пробное занятие'
        }
        return redirect(url_for('sent', context=json.dumps(context)))

    context = {
        'name': teacher['name'],
        'picture': teacher['picture'],
        'teacher_id': teacher_id,
        'lesson_day': RU_DAYS[request.args.get('day')],
        'lesson_time': request.args.get('time')
    }

    return render_template('booking.html', form=form, **context)


@app.route('/teacher_selection', methods=['GET', 'POST'])
def teacher_selection():
    form = TeacherSelectionForm()
    
    if form.validate_on_submit():
        update_data_in_file(
            'requests',
            {'name': form.name.data,
             'phone': form.phone.data,
             'goal': form.goals.data,
             'time': form.time.data}
        )
        context = {
            'name': form.name.data,
            'phone': form.phone.data,
            'goal': GOALS[form.goals.data],
            'time': form.time.data,
            'subject': 'request',
            'subject_description': 'Заявка на подбор преподавателя'
        }
        return redirect(url_for('sent', context=json.dumps(context)))

    return render_template('pick.html', form=form)


@app.route('/message/<string:teacher_id>', methods=['GET', 'POST'])
def message(teacher_id):
    teacher = TEACHERS.get(teacher_id)
    if not teacher:
        abort(404)

    form = MessageForm()

    if form.validate_on_submit():
        flash('Сообщение отправлено!', category='sent')
        return redirect(url_for('message', teacher_id=teacher_id))
        
    context = {'teacher': teacher, 'teacher_id': teacher_id}
    return render_template('message.html', form=form, **context)


@app.errorhandler(404)
def not_found(error):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"

