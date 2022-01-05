from genius import search, get_text
from aiogram import types

start_aw = '''Привет, добро пожаловать, я бот, который помогает находить текста песен
Введи @lyricstgbot и начни писать название песни, я подскажу, что нашел
'''


def build_query_aw(q_str: str) -> list:
    """Build query list for send to user

    Args:
        q_str (str): search query

    Returns:
        list: list for sending
    """
    result = []
    if len(q_str) == 0:
        return result
    else:
        tracks = search(q_str)
        id = 0
        for track in tracks['songs']:
            name = track['title']
            artist = track['artist']
            track_id = int(track['api_path'].split('/')[-1])
            title = f'{name} ({artist})'
            if track['pageviews']:
                views = track['pageviews']
                description = f'Запросов: {views}'
            else:
                description = None

            result.append(
                types.InlineQueryResultArticle(
                    id=str(id),
                    title=title,
                    description=description,
                    input_message_content=types.InputTextMessageContent(
                        message_text=(f'/track{track_id}')
                    ),
                    thumb_url=track['image']
                )
            )
            id += 1

    return result


def lyrics_aw(id: int):
    api_path = f'/songs/{id}'
    return get_text(api_path)
