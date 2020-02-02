from config import stop_bus
from datetime import datetime


def cleaning_post(data: tuple):
    for date in data:
        if ('чисто' in date[0]) or ('как' in date[0]) or ('актуально?' in date[0]) or ('cтоят на' in date[0]):
            pass
        else:
            temporary_tuple = (date[0].replace(',', '').replace('\n', '').replace('-', ' ').replace('!', ''), date[1])
            yield temporary_tuple


def cleaning_post_otherwise(data: tuple):
    for date in data:
        if 'чисто' in date[0]:
            temporary_tuple = (date[0].replace(',', '').replace('\n', '').replace('-', ' ').replace('!', ''), date[1])
            yield temporary_tuple


def validation_bus_stop(data: tuple):
    """ Поиск остановки в строчке"""
    temp_data = []
    for _data in data:
        dates = _data[0].split()
        for i in range(len(dates)):
            for j in range(i, len(dates)):
                combination = ' '.join(dates[i:j + 1])
                if combination in stop_bus:
                    temporary_tuple = (combination, _data[1])
                    temp_data.append(temporary_tuple)
    return temp_data


def sort_busstop(data: tuple, _sort=None, time_format='%H:%M'):
    """ Сортировка генератора по определенному критерию """
    time_data = {}
    for date in data:
        if date['bus_stop'] not in time_data:
            time_data.update({date['bus_stop']: [1, datetime.fromtimestamp(date['time']).strftime(time_format)]})
        else:
            _time_data = time_data.get(date['bus_stop'])
            time_data.update({date['bus_stop']: [_time_data[0] + 1, datetime.fromtimestamp(date['time']).strftime(time_format)]})
    sort = 1
    if _sort == "Сообщения":
        sort = 0
    elif _sort in ['none', 'no', 'not']:
        return time_data

    return dict(sorted(time_data.items(), key=lambda x: x[1][sort], reverse=True))
