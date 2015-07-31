import os
import json

from babynames import scraper

CACHE_DIR = os.path.join(os.path.abspath('.'), '_cache')
CACHE_FILENAME_FORMAT = '%s.txt'
EMPTY_CACHE = ({}, {})


def get(year, url):
    cached_value = _get_from_cache(year)
    if any(cached_value):
        return cached_value

    web_value = _get_from_web(year, url)
    _save_to_cache(year, web_value)
    return web_value


def _get_from_web(year, url):
    return scraper.get(year, url)


def _get_from_cache(year):
    cache_file_path = os.path.join(CACHE_DIR, CACHE_FILENAME_FORMAT % year)
    if os.path.exists(cache_file_path):
        cache_file = open(cache_file_path)
        return json.load(cache_file)
    return EMPTY_CACHE


def _save_to_cache(year, data):
    # don't save empty data
    if not any(data):
        return
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)
    cache_file_path = os.path.join(CACHE_DIR, CACHE_FILENAME_FORMAT % year)
    cache_file = open(cache_file_path, 'w')
    json.dump(data, cache_file)
