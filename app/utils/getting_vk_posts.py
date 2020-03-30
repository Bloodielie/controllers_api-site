from app.utils.vk_api import VkApi
import asyncio


async def get_post_wall(vk: VkApi, count: int = 100, group_id: int = 72869598):
    wall: dict = await vk.method('wall.get', owner_id=-group_id, count=count)
    data = []
    for items in wall['items']:
        data.append((items['text'].lower(), items['date']))
    return data


async def get_comment_data(vk: VkApi, group_id: int):
    wall: dict = await vk.method('wall.get', owner_id=-group_id, count=2)
    await asyncio.sleep(1)
    post_id: int = wall['items'][0]['id']
    post_id_2: int = wall['items'][1]['id']
    comment_count: int = wall['items'][0]['comments']['count']
    comment_offset: int = 0
    if comment_count > 100:
        comment_offset: int = comment_count - 100
    comments: list = (await vk.method('wall.getComments', owner_id=-group_id, post_id=post_id, count=100,
                                      offset=comment_offset)).get('items')
    await asyncio.sleep(1)
    comments2: list = (await vk.method('wall.getComments', owner_id=-group_id, post_id=post_id_2, count=100,
                                       offset=comment_offset)).get('items')
    comments.extend(comments2)
    data = []
    for comment in comments:
        try:
            data.append((comment['text'].lower(), comment['date']))
        except KeyError:
            continue
    return data
