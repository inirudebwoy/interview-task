try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from babynames import proxy


EMPTY_RESPONSE = ({}, {})
VALID_RESPONSE = ({'Michael': 7}, {'Emily': 7})


class TestProxyGet:
    @patch('babynames.proxy.scraper.get', return_value=EMPTY_RESPONSE)
    def test_get_returns_tuple_of_empty_dicts(self, scraper_mock):
        assert proxy.get(2014, 'www.url.com') == ({}, {})

    @patch('babynames.proxy.scraper.get', return_value=VALID_RESPONSE)
    def test_get_returns_tuple_of_dicts_with_data(self, scraper_mock):
        dict_one, dict_two = proxy.get(2014, 'www.url.com')
        for name, rank in dict_one.update(dict_two):
            assert isinstance(name, str)
            assert isinstance(rank, int)


class TestScraperCommunication:
    @patch('babynames.proxy.scraper.get', return_value=EMPTY_RESPONSE)
    def test_get_from_web_returns_tuple_of_empty_dicts(self, scraper_mock):
        assert proxy._get_from_web(2014, 'www.url.com') == ({}, {})

    @patch('babynames.proxy.scraper.get', return_value=VALID_RESPONSE)
    def test_get_from_web_returns_tuple_with_valid_data(self, scraper_mock):
        dict_one, dict_two = proxy._get_from_web(2014, 'www.url.com')
        for name, rank in dict_one.update(dict_two):
            assert isinstance(name, str)
            assert isinstance(rank, int)


class TestCacheCommunication:
    @patch('babynames.proxy.scraper.get', return_value=EMPTY_RESPONSE)
    def test_get_from_cache_returns_empty_tuple(self, scraper_mock):
        assert proxy._get_from_cache(2014, 'www.url.com') == ({}, {})

    @patch('babynames.proxy.scraper.get', return_value=VALID_RESPONSE)
    def test_get_from_cache_returns_tuple_with_valid_data(self, scraper_mock):
        dict_one, dict_two = proxy._get_from_cache(2014, 'www.url.com')
        for name, rank in dict_one.update(dict_two):
            assert isinstance(name, str)
            assert isinstance(rank, int)

    def test_save_to_cache_no_cache_dir(self):
        pass

    def test_save_to_cache_with_cache_dir(self):
        pass
