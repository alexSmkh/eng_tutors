import json

from flask import render_template, abort, request, url_for, redirect, flash

from app import app, db 
from app.models import Teacher, Goal, Request, Booking
from app.forms import BookingForm, TeacherSelectionForm, MessageForm
from tools import update_data_in_file
from global_variables import TEACHERS, GOALS, EMOJI, RU_DAYS_SHORT, RU_DAYS



@app.route('/')
def main():
    ordered_teacher_ids_by_rating = sorted(
        TEACHERS,
        key=lambda teacher_id: TEACHERS[teacher_id]['rating'],
        reverse=True
    )
    
    ordered_teachers = {id_: TEACHERS[id_] for id_ in ordered_teacher_ids_by_rating}
    context = {
        'teachers': ordered_teachers,
        'goals': GOALS,
        'emoji': EMOJI
    }
    return render_template('index.html', **context)


@app.route('/goals/<goal>')
def goal(goal):
    teachers = {
        id_: teacher 
        for id_, teacher in TEACHERS.items() 
        if goal in teacher['goals']
    }

    ordered_teacher_ids_by_rating = sorted(
        teachers,
        key=lambda teacher_id: teachers[teacher_id]['rating'],
        reverse=True
    )

    ordered_teachers = {id_: TEACHERS[id_] for id_ in ordered_teacher_ids_by_rating}

    context = {
        'teachers': ordered_teachers,
        'emoji': EMOJI[goal],
        'goal': GOALS[goal]
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

