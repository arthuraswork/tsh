from newlib.define import Module
import datetime
import random

content = {
    '#time': lambda: datetime.now().strftime('%H:%M:%S'),
    '#date': lambda: datetime.now().strftime('%Y-%m-%d'),
    '#rdate': lambda: datetime.now().strftime('%d-%m-%Y'),
    '#dayofweek': lambda: datetime.now().isoweekday(),
    '#randint2': lambda: random.randint(0,1),
    '#randint4': lambda: random.randint(0,3),
    '#randint8': lambda: random.randint(0,7),
    '#randint16': lambda: random.randint(0,15),
}

objects = Module('objects',content) 