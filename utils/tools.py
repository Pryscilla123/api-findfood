import pytz
from enum import Enum
from datetime import datetime


class Days(Enum):
    SEGUNDA = 'Monday'
    TERCA = 'Tuesday'
    QUARTA = 'Wednesday'
    QUINTA = 'Thursday'
    SEXTA = 'Friday'
    SABADO = 'Saturday'
    DOMINGO = 'Sunday'
    MONDAY = 'Segunda'
    TUESDAY = 'Terca'
    WEDNESDAY = 'Quarta'
    THURSDAY = 'Quinta'
    FRIDAY = 'Sexta'
    SATURDAY = 'Sabado'
    SUNDAY = 'Domingo'


def is_in_the_interval(open, close, format='%H:%M', date=datetime.now()):
    x1 = datetime.strptime(open, format).time()
    x2 = datetime.strptime(close, format).time()

    if x1 <= date.time() <= x2:
        return True

    return False


if __name__ == '__main__':
    is_open = is_in_the_interval(open='12:00', close='18:00')

