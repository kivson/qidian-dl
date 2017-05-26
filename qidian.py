from concurrent.futures import ThreadPoolExecutor
from functools import partial
from json import JSONDecodeError

import requests
from funcy.calc import cache
from funcy.debug import print_calls
from funcy.simple_funcs import curry

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
HOME_URL = "https://www.webnovel.com/"


class QidianException(Exception):
    pass


@cache(60)
def _get_csrftoken():
    response = requests.get(HOME_URL)
    return response.cookies.get('_csrfToken', None)


def novels():
    for page in range(1, 10000):
        response = requests.get("https://www.webnovel.com/apiajax/listing/popularAjax", headers=HEADERS, params={
            '_csrfToken': _get_csrftoken(),
            'category': '',
            'pageIndex': page
        })

        data = _response_to_json(response)

        if 'data' not in data or 'items' not in data['data'] or 'isLast' not in data['data']:
            raise QidianException('Expected data not found')

        yield from data['data']['items']

        if data['data']['isLast'] == 1:
            break


def _response_to_json(response):
    try:
        data = response.json()
    except JSONDecodeError:
        raise QidianException('Json parse Error')
    return data


def charpters_list(bookId):
    response = requests.get('https://www.webnovel.com/apiajax/chapter/GetChapterList', headers=HEADERS, params={
        '_csrfToken': _get_csrftoken(),
        'bookId': bookId
    })

    data = _response_to_json(response)

    if 'data' not in data or 'chapterItems' not in data['data']:
        raise QidianException('Expected data not found')

    yield from data['data']['chapterItems']


def chapter(bookId, chapterId):
    response = requests.get('https://www.webnovel.com/apiajax/chapter/GetContent', headers=HEADERS, params={
        '_csrfToken': _get_csrftoken(),
        'bookId': bookId,
        'chapterId': chapterId
    })

    data = _response_to_json(response)

    if 'data' not in data or 'chapterInfo' not in data['data']:
        raise QidianException('Expected data not found')

    return data['data']['chapterInfo']


def all_chapters(bookId, poolsize=10):
    charpters = charpters_list(bookId=bookId)
    with ThreadPoolExecutor(max_workers=poolsize) as executor:
        chapter_getter = partial(chapter, bookId)
        yield from executor.map(chapter_getter, (c['chapterId'] for c in charpters))
