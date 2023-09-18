from datetime import datetime
from calendar import isleap
import threading


def months(year: int) -> dict:
    mon = {'янв': {'num': 1, 'days': 31},
            'фев': {'num': 2, 'days': 28 + int(isleap(year))},
            'мар': {'num': 3, 'days': 31},
            'апр': {'num': 4, 'days': 30},
            'май': {'num': 5, 'days': 31},
            'июн': {'num': 6, 'days': 30},
            'июл': {'num': 7, 'days': 31},
            'авг': {'num': 8, 'days': 31},
            'сен': {'num': 9, 'days': 30},
            'окт': {'num': 10, 'days': 31},
            'нояб': {'num': 11, 'days': 30},
            'дек': {'num': 12, 'days': 31}}
    return mon

name_of_month = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'нояб', 'дек']

s = '2023-12-27 16:00:00'
date = s[:10]
time = s[11:16]

m = months(int(s[:4]))

print(s[8:10] + ' ' + name_of_month[int(s[5:7]) - 1])
