from datetime import datetime
from typing import Tuple, Union, Iterator

from app.configuration.config import clean_dirty_word, clean_clean_word
from abc import ABC, abstractmethod


class PostCleanerAbstract(ABC):
    @abstractmethod
    def cleaning_posts(self, posts: Iterator[tuple], type_cleaning: str) -> Iterator[Tuple[str, int]]:
        raise NotImplementedError


class PostCleaner(PostCleanerAbstract):
    def cleaning_posts(self, posts: Iterator[tuple], type_cleaning: str) -> Iterator[Tuple[str, int]]:
        for post in posts:
            word: str = self.cleaning_words(post[0])
            for iteration_value, word_data in enumerate(word.split()):
                if type_cleaning == 'dirty':
                    if word_data in clean_dirty_word:
                        break
                    if iteration_value >= len(word.split()) - 1:
                        yield word, post[1]
                elif type_cleaning == 'clean':
                    if word_data in clean_clean_word:
                        yield word, post[1]
                        break
                else:
                    raise Exception('Incorrect cleaning type indicated')

    @staticmethod
    def cleaning_words(string: str) -> str:
        return string.replace(',', '').replace('\n', '').replace('-', ' ').replace('!', '').lower()


def validation_bus_stop(data: Iterator[tuple], stop_bus: list) -> list:
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


def sort_busstop(data: Union[list, tuple], _sort=None, time_format: str = '%H:%M') -> dict:
    """ Сортировка генератора по определенному критерию """
    time_data = {}
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
