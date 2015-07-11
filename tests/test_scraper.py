import os
import codecs
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from requests import Request, Response, Session
from bs4 import BeautifulSoup
from babynames import scraper


LOCAL_URL = "http://127.0.0.1"
THIS_DIR = os.path.dirname(__file__)


class TestScraper:

    _example_html = None

    @property
    def example_html(self):
        """
        Loads the HTML from the example file and returns it as bytes, just as requests like it.
        """
        if not self._example_html:
            with codecs.open(os.path.join(THIS_DIR, "names2014.html"), encoding='utf-8') as f:
                self._example_html = codecs.encode(f.read())
        return self._example_html

    def test_get_takes_year_arg(self):
        """
        get() should take a 'year' argument.
        """
        scraper.get(year=2000)

    def test_create_request_takes_year_and_url_args(self):
        """
        _create_request() should take the 'year' and 'url' arguments.
        """
        scraper._create_request(year=2000, url=LOCAL_URL)

    def test_create_request_creates_request(self):
        """
        _create_request() should return a requests.models.Request object.
        """
        req = scraper._create_request(year=2000, url=LOCAL_URL)
        assert isinstance(req, Request)

    def test_create_request_creates_POST_req(self):
        """
        _create_request() should create a POST request.
        """
        req = scraper._create_request(year=2000, url=LOCAL_URL)
        assert req.method == "POST"

    def test_create_request_creates_POST_req_with_year_form_var(self):
        """
        _create_request() should create a POST request which includes a 'year' form variable.
        """
        year = 2000
        req = scraper._create_request(year=year, url=LOCAL_URL)
        assert "year" in req.data
        assert req.data["year"] == year

    def test_create_request_creates_POST_req_with_top_form_var_default(self):
        """
        _create_request() should create a POST request which includes a 'top' form variable
        which defaults to 1000.
        """
        req = scraper._create_request(year=2000, url=LOCAL_URL)
        assert "top" in req.data
        assert req.data["top"] == 1000

    def test_create_request_creates_POST_req_with_top_form_var_set(self):
        """
        _create_request() should create a POST request which includes a 'top' form variable
        which is specifically set to 500.
        """
        req = scraper._create_request(year=2000, url=LOCAL_URL, top=500)
        assert "top" in req.data
        assert req.data["top"] == 500

    def test_perform_request_performs_request(self):
        """
        _perform_request() should perform the request and return a Response object.
        """
        req = scraper._create_request(year=2000, url=LOCAL_URL)
        with patch.object(Session, "send", return_value=Response()):
            resp = scraper._perform_request(req)
        assert isinstance(resp, Response)

    def test_perform_request_performs_request_and_gets_data(self):
        """
        _perform_request() should perform the request and return a Response object which
        contains the correct HTML.
        """
        req = scraper._create_request(year=2000, url=LOCAL_URL)
        fake_resp = Response()
        fake_resp._content = self.example_html
        with patch.object(Session, "send", return_value=fake_resp):
            resp = scraper._perform_request(req)
        assert resp.text == fake_resp.text

    def test_parse_response_returns_beautifulsoup_object(self):
        """
        _parse_response should return a BeautifulSoup object.
        """
        resp = Response()
        resp._content = self.example_html
        bs = scraper._parse_response(resp)
        assert isinstance(bs, BeautifulSoup)
