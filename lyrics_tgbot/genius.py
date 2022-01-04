import requests
from bs4 import BeautifulSoup

# session and user-agent
http = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}


def get_html(url: str, params: dict) -> str:
    """function for getting html of page

    Args:
        url (str): link to page
        params (dict): params to send

    Returns:
        str: text of page
    """
    return http.get(url, params=params, headers=headers).text


def dict_builder(data: dict) -> dict:
    """function for building dict of parsed data

    Args:
        data (dict): parse data

    Returns:
        dict: builded dict
    """
    try:
        pageviews = data['stats']['pageviews']
    except KeyError:
        pageviews = None

    return {'title': data['title'], 'artist': data['primary_artist']['name'],
            'api_path': data['api_path'], 'pageviews': pageviews, 'image': data['header_image_thumbnail_url']}


def search(q_str: str) -> dict:
    """search in genius

    Args:
        q_str (str): query string

    Returns:
        dict: search response
    """
    data = {'songs': [], 'lyric': []}
    response = http.get(
        'https://genius.com/api/search/multi?per_page=5', params={'q': q_str}, headers=headers).json()

    sections = response['response']['sections']
    if len(sections[1]['hits']) == 0 and len(sections[2]) == 0:
        return False

    for section in response['response']['sections'][1:3]:
        if section['type'] == 'song':
            for song in section['hits']:
                music = song['result']
                # print(music)
                if len(data['songs']) == 0:
                    data['songs'].append(dict_builder(music))
                if data['songs'][-1]['api_path'] != music['api_path']:
                    data['songs'].append(dict_builder(music))

        elif section['type'] == 'lyric':
            for lyric in section['hits']:
                music = lyric['result']
                if len(data['lyric']) == 0:
                    data['lyric'].append(dict_builder(music))
                if data['lyric'][-1]['api_path'] != music['api_path']:
                    data['songs'].append(dict_builder(music))

    return data


def get_text(api_path: str) -> str:
    """function get lyrics of track by api_path

    Args:
        api_path (str): link to track

    Returns:
        str: format lyrics
    """
    html = get_html('https://genius.com{}'.format(api_path), None)
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find(
        'div', {'class': 'Lyrics__Container-sc-1ynbvzw-6 lgZgEN'})
    str_container = str(container).replace('<br/>', '\n')
    container = BeautifulSoup(str_container, "html.parser")
    lyrics = container.text
    return lyrics