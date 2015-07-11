try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from requests import Request, Response, Session
from babynames import scraper


LOCAL_URL = "http://127.0.0.1"


class TestScraper:

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
