import os
import shutil
import json
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from babynames import proxy

import pytest

EMPTY_RESPONSE = ({}, {})
VALID_RESPONSE = ({'Michael': 7}, {'Emily': 7})
YEAR = 2014


@pytest.fixture
def clear_cache():
    if os.path.exists(proxy.CACHE_DIR):
        shutil.rmtree(proxy.CACHE_DIR)


@pytest.fixture
def set_cache():
    if not os.path.exists(proxy.CACHE_DIR):
        os.mkdir(proxy.CACHE_DIR)
    cache_file_path = os.path.join(proxy.CACHE_DIR,
                                   proxy.CACHE_FILENAME_FORMAT % YEAR)
    cache_file = open(cache_file_path, 'w')
    json.dump(VALID_RESPONSE, cache_file)
    cache_file.close()


class TestProxyGet:
    @patch('babynames.proxy.scraper.get', return_value=EMPTY_RESPONSE)
    @patch('babynames.proxy._get_from_cache', return_value=EMPTY_RESPONSE)
    def test_get_returns_tuple_of_empty_dicts(self, scraper_mock, cache_mock):
        assert proxy.get(YEAR, 'www.url.com') == EMPTY_RESPONSE

    @patch('babynames.proxy.scraper.get', return_value=VALID_RESPONSE)
    @patch('babynames.proxy._get_from_cache', return_value=VALID_RESPONSE)
    def test_get_returns_tuple_of_dicts_with_data(self, scraper_mock,
                                                  cache_mock):
        dict_one, dict_two = proxy.get(YEAR, 'www.url.com')
        assert isinstance(dict_one, dict)
        assert isinstance(dict_two, dict)
        assert dict_one
        assert dict_two


class TestScraperCommunication:
    @patch('babynames.proxy.scraper.get', return_value=EMPTY_RESPONSE)
    def test_get_from_web_returns_tuple_of_empty_dicts(self, scraper_mock):
        assert proxy._get_from_web(YEAR, 'www.url.com') == EMPTY_RESPONSE

    @patch('babynames.proxy.scraper.get', return_value=VALID_RESPONSE)
    def test_get_from_web_returns_tuple_with_valid_data(self, scraper_mock):
        dict_one, dict_two = proxy._get_from_web(YEAR, 'www.url.com')
        assert isinstance(dict_one, dict)
        assert isinstance(dict_two, dict)
        assert dict_one
        assert dict_two


class TestCacheCommunication:
    def test_get_from_cache_returns_empty_tuple(self, clear_cache):
        assert proxy._get_from_cache(YEAR) == EMPTY_RESPONSE

    def test_get_from_cache_returns_tuple_with_valid_data(self, set_cache):
        dict_one, dict_two = proxy._get_from_cache(YEAR)
        assert isinstance(dict_one, dict)
        assert isinstance(dict_two, dict)
        assert dict_one
        assert dict_two


class TestCacheOperations:
    def test_save_to_cache_no_cache_dir(self, clear_cache):
        cache_file_path = os.path.join(proxy.CACHE_DIR,
                                       proxy.CACHE_FILENAME_FORMAT % YEAR)

        proxy._save_to_cache(YEAR, VALID_RESPONSE)
        assert os.path.exists(cache_file_path)

    def test_save_to_cache_with_cache_dir(self, clear_cache):
        os.mkdir(proxy.CACHE_DIR)
        cache_file_path = os.path.join(proxy.CACHE_DIR,
                                       proxy.CACHE_FILENAME_FORMAT % YEAR)

        proxy._save_to_cache(YEAR, VALID_RESPONSE)
        assert os.path.exists(cache_file_path)
