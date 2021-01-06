import asyncio
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.emoji import emojize
from instalooter.looters import PostLooter

logging.basicConfig(level=logging.ERROR)

API_TOKEN = os.environ['API_TOKEN']

HELP_MESSAGE = \
'''
Привет, я умею скачивать фото и видео из Instagram!

Для того, чтобы скачать фото или видео отправь мне ссылку на пост. \
В ответ я пришлю тебе всё содержимое этого поста.

Нашёл ошибку или есть предложения по улучшению бота? Пиши: @ijustbsd
'''

ERROR_MESSAGE = \
'''
Что-то пошло не так :pensive_face: Возможно указана неверная ссылка на пост или данный аккаунт закрыт.
'''

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def get_links(media, looter):
    if media.get('__typename') == 'GraphSidecar':
        media = looter.get_post_info(media['shortcode'])
        nodes = [e['node'] for e in media['edge_sidecar_to_children']['edges']]
        return [n.get('video_url') or n.get('display_url') for n in nodes]
    elif media['is_video']:
        media = looter.get_post_info(media['shortcode'])
        return [media['video_url']]
    else:
        return [media['display_url']]


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(HELP_MESSAGE)


@dp.message_handler()
@dp.throttled(rate=1)
async def send_media(message: types.Message):
    try:
        looter = PostLooter(message.text, get_videos=True)
        edges = looter.info['edge_media_to_caption']['edges']
    except (ValueError, KeyError):
        await message.answer(emojize(ERROR_MESSAGE))
        return

    media = types.MediaGroup()
    for m in looter.medias():
        for link in get_links(m, looter):
            if '.mp4' in link:
                media.attach_video(link)
            else:
                media.attach_photo(link)

    await message.answer_media_group(media=media)

    try:
        description = edges[0]['node']['text']
        await message.answer(description)
    except IndexError:
        await message.answer('<i>Описание отсутствует.</i>', parse_mode=types.ParseMode.HTML)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
