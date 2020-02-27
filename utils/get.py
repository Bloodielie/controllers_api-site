from vk_api import VkApi
from typing import Tuple


def get_post_wall(vk: VkApi, count: int = 100, group_id: int = 72869598) -> Tuple[str, int]:
    """ Получения постов """
    wall: dict = vk.method('wall.get', values={'owner_id': -group_id, 'count': count})
    for items in wall['items']:
        temporary_tuple = (items['text'].lower(), items['date'])
        yield temporary_tuple


def get_comment_data(vk: VkApi, group_id: int) -> Tuple[str, int]:
    wall: dict = vk.method('wall.get', values={'owner_id': -group_id, 'count': 2})
    post_id: int = wall['items'][0]['id']
    post_id_2: int = wall['items'][1]['id']
    comment_count: int = wall['items'][0]['comments']['count']
    comment_offset: int = 0
    if comment_count > 100:
        comment_offset: int = comment_count - 100
    comments: list = vk.method('wall.getComments', values={'owner_id': -group_id, 'post_id': post_id, 'count': 100, 'offset': comment_offset})['items']
    comments2: list = vk.method('wall.getComments', values={'owner_id': -group_id, 'post_id': post_id_2, 'count': 100, 'offset': comment_offset})['items']
    comments.extend(comments2)
    for comment in comments:
        try:
            yield comment['text'].lower(), comment['date']
        except KeyError:
            continue
