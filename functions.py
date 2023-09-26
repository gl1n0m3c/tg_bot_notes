from DB.executes import Executions
from datetime import datetime, timedelta, timezone
from calendar import isleap 
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from input import PATH



offset = timedelta(hours=3)
tz = timezone(offset = offset, name = 'МСК')
BASE = Executions(PATH)
name_of_month = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'нояб', 'дек']
months = {'янв': {'num': '01', 'days': 31},
          'фев': {'num': '02', 'days': 28 + int(isleap(datetime.now().year))},
          'мар': {'num': '03', 'days': 31},
          'апр': {'num': '04', 'days': 30},
          'май': {'num': '05', 'days': 31},
          'июн': {'num': '06', 'days': 30},
          'июл': {'num': '07', 'days': 31},
          'авг': {'num': '08', 'days': 31},
          'сен': {'num': '09', 'days': 30},
          'окт': {'num': '10', 'days': 31},
          'нояб': {'num': '11', 'days': 30},
          'дек': {'num': '12', 'days': 31}}


def all_notes() -> str:
    data = BASE.give_all_data()
    TEXT = ''
    for note in data:
        date = note[1]
        TEXT += (f'Уникальный номер: <b>{note[0]}</b>. Дата: <b>{date[8:10]} {name_of_month[int(date[5:7]) - 1]} {date[11:16]}</b>; Заметка: <b>{note[2]}</b>\n')
    
    if len(data) == 0:
        return 'Вы еще не добавили никаких заметок!'
    else:
        return f'Вот список всех ваших заметок:\n{TEXT}\n'


def save_note(mes: list, permanent: bool = False) -> int:
    try:
        datetime.strptime(f'{datetime.now().year}-{months[mes[1]]["num"]}-{mes[0]} {mes[2]}:00', "%Y-%m-%d %H:%M:%S")
    
    except:
        return 0
    
    else:
        if len(mes[2]) == 4:
            mes[2] = '0' + mes[2]
            
        year = datetime.now(tz=tz).year
        date = f'{year}-{months[mes[1]]["num"]}-{mes[0]} {mes[2]}:00'
        if date < str(datetime.now(tz=tz)):
            date = f'{year + 1}-{months[mes[1]]["num"]}-{mes[0]} {mes[2]}:00'

        text = ''
        if len(mes) > 3:
            for el in mes[3:]:
                text += (el + ' ')

        if permanent == False:
            BASE.insert_data(date, text)
        else:
            BASE.insert_data(date, text, 1)
        return 1


def del_note(num):  # можно оформить через binsearch
    try:
        int(num)
    except:
        return 'Введен неверный формат, повторите попытку:'
    else:
        data = BASE.give_all_data()
        for note in data:
            if note[0] == int(num):
                break
        else:
            return 'Данной записи не существует!\nПопробуйте снова:'
        BASE.del_note(num)
        return 1


def nearest_note():
    note = BASE.give_nearest_note()
    if len(note) == 0:
        return 'Вы еще не добавили никаких заметок!'
    note = note[0]
    date = note[1]
    text = 'Ближайшее событие:\n' + \
          f'Уникальный номер: <b>{note[0]}</b>. Дата: <b>{date[8:10]} {name_of_month[int(date[5:7]) - 1]} {date[11:16]}</b>; Заметка: <b>{note[2]}</b>\n'
    return text


def make_buttons(value: list):
    buttons = [[]]
    i = j = 0
    for el in value:
        buttons[i].append(KeyboardButton(text = el))
        j += 1
        if j % 2 == 0:
            i += 1
            buttons.append([])
    keyboard = ReplyKeyboardMarkup(keyboard = buttons, one_time_keyboard = True, resize_keyboard = True)
    return keyboard


def need_to_remind():
    note = BASE.give_nearest_note()
    if len(note) != 0:
        note = note[0]

        while note[1][:16] < str(datetime.now(tz=tz))[:16]:
            del_note(int(note[0]))
            note = BASE.give_nearest_note()
            if len(note) == 0:
                break
            note = note[0]

        if len(note) != 0:
            if note[1][:16] == str(datetime.now(tz=tz))[:16]:
                if note[3] == 0:
                    del_note(int(note[0]))
                else:
                    date = datetime.now() + timedelta(days=1)
                    date = str(date)[:-7]
                    print(f'{date[8:10]} {name_of_month[int(date[5:7]) - 1]} {date[11:16]} {note[2]}')
                    save_note((f'{date[8:10]} {name_of_month[int(date[5:7]) - 1]} {date[11:16]} {note[2]}').split(), True)
                return note[2]
    return 0


