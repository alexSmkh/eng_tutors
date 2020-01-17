import json
import os

from tools import read_file


TEACHERS = json.loads(
    read_file(os.path.join(os.getcwd(), 'data/teachers.json'))
)
GOALS = json.loads(
    read_file(os.path.join(os.getcwd(), 'data/goals.json'))
)
EMOJI = {
    'study': u'\U0001F3EB',
    'work': u'\U0001F3E2', 
    'travel': u'\U0001F5FA',
    'relocate': u'\U0001F69C'
}


RU_DAYS_SHORT = {
    'mon': 'Пн', 
    'tue': 'Вт', 
    'wed': 'Ср', 
    'thu': 'Чт', 
    'fri': 'Пт', 
    'sat': 'Сб', 
    'sun': 'Вс'
}
RU_DAYS = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда', 
    'thu': 'Четверг', 
    'fri': 'Пятница', 
    'sat': 'Суббота', 
    'sun': 'Воскресенье'
}
