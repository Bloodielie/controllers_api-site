def get_post_wall(vk, count=100, group_id=72869598):
    """ Получения постов """
    wall = vk.method('wall.get', values={'owner_id': -group_id, 'count': count})
    for i in wall['items']:
        temporary_tuple = (i['text'].lower(), i['date'])
        yield temporary_tuple


def get_comment_data(vk, group_id):
    wall = vk.method('wall.get', values={'owner_id': -group_id, 'count': 2})
    post_id = wall['items'][0]['id']
    post_id_2 = wall['items'][1]['id']
    comment_count = wall['items'][0]['comments']['count']
    comment_offset = 0
    if comment_count > 100:
        comment_offset = comment_count - 100
    comments = vk.method('wall.getComments', values={'owner_id': -group_id, 'post_id': post_id, 'count': 100, 'offset': comment_offset})['items']
    comments2 = vk.method('wall.getComments', values={'owner_id': -group_id, 'post_id': post_id_2, 'count': 100, 'offset': comment_offset})['items']
    comments.extend(comments2)
    for comment in comments:
        try:
            yield comment['text'].lower(), comment['date']
        except KeyError:
            continue
