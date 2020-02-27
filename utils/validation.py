from config import clean_dirty_word, clean_clean_word
from datetime import datetime
from typing import Tuple


def cleaning_words(string: str) -> str:
    return string.replace(',', '').replace('\n', '').replace('-', ' ').replace('!', '').lower()


def cleaning_post(data: tuple) -> Tuple[str, int]:
    for date in data:
        word: str = cleaning_words(date[0])
        for iteration_value, word_data in enumerate(word.split()):
            if word_data in clean_dirty_word:
                break
            if iteration_value >= len(word.split())-1:
                temporary_tuple: tuple = (word, date[1])
                yield temporary_tuple


def cleaning_post_otherwise(data: tuple) -> Tuple[str, int]:
    for date in data:
        word: str = cleaning_words(date[0])
        for iteration_value, word_data in enumerate(word.split()):
            if word_data in clean_clean_word:
                temporary_tuple: tuple = (word, date[1])
                yield temporary_tuple
                break


def validation_bus_stop(data: tuple, stop_bus: list) -> list:
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


def sort_busstop(data: tuple, _sort=None, time_format: str = '%H:%M') -> dict:
    """ Сортировка генератора по определенному критерию """
    time_data: dict = {}
    for date in data:
        if date['bus_stop'] not in time_data:
            time_data.update({date['bus_stop']: [1, datetime.fromtimestamp(date['time']).strftime(time_format)]})
        else:
            _time_data = time_data.get(date['bus_stop'])
            time_data.update({date['bus_stop']: [_time_data[0] + 1, datetime.fromtimestamp(date['time']).strftime(time_format)]})
    sort: int = 1
    if _sort == "Сообщения":
        sort: int = 0
    elif str(_sort).lower() in ['none', 'no', 'not']:
        return time_data

    return dict(sorted(time_data.items(), key=lambda x: x[1][sort], reverse=True))
