from babynames import scraper

CACHE_DIR = '_cache'


def get(year, url):
    cached_value = _get_from_cache(year, url)
    if any(cached_value):
        return cached_value

    web_value = _get_from_web(year, url)
    _save_to_cache(web_value)
    return web_value


def _get_from_web(year, url):
    return scraper.get(year, url)


def _get_from_cache(year, url):
    pass


def _save_to_cache(data):
    pass
