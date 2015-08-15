import os
import json
import errno

from babynames import scraper

CACHE_DIR = os.path.join(os.path.abspath('.'), '_cache')
CACHE_FILENAME_FORMAT = '%s.txt'
EMPTY_CACHE = ({}, {})


def get(year, url):
    """Get data for year from url.

    Function will reach to cache and check if data has been already
    fetched. If not data will be retrieved from web and stored to cache.

    :param year: get data from following year
    :type year: str
    :param url: url where get data from
    :type url: str
    :returns: data, names with ranks
    :rtype: ({}, {})

    """
    cached_value = _get_from_cache(year)
    if any(cached_value):
        return cached_value

    web_value = _get_from_web(year, url)
    _save_to_cache(year, web_value)
    return web_value


def _get_from_web(year, url):
    """Retrieve data from url for following year

    :param year: get data from following year
    :type year: str
    :param url: url where get data from
    :type url: str
    :returns: data from web, names with ranks
    :rtype: ({}, {})

    """
    return scraper.get(year, url)


def _get_from_cache(year):
    """Retrieve data from cache for following year

    :param year: get data from following year
    :type year: str
    :returns: data from cache, names with ranks
    :rtype: ({}, {})

    """
    cache_file_path = os.path.join(CACHE_DIR, CACHE_FILENAME_FORMAT % year)
    try:
        cache_file = open(cache_file_path)
    except IOError:
        return EMPTY_CACHE
    return json.load(cache_file)


def _save_to_cache(year, data):
    """Save data to cache

    :param year: get data from following year
    :type year: str
    :param data: data to be saved into cache
    :type data: tuple with two dictionaries ({}, {})

    """
    # don't save empty data
    if not any(data):
        return

    try:
        os.makedirs(CACHE_DIR)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    cache_file_path = os.path.join(CACHE_DIR, CACHE_FILENAME_FORMAT % year)
    cache_file = open(cache_file_path, 'w')
    json.dump(data, cache_file)
