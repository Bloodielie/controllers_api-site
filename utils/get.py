def get_post(vk, count=100, group_id=72869598):
    """ Получения постов """
    wall = vk.method('wall.get', values={'owner_id': -group_id, 'count': count})
    for i in wall['items']:
        temporary_tuple = (i['text'].lower(), i['date'])
        yield temporary_tuple
