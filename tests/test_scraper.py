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

    def test_create_request_creates_POST_request_with_year_form_variable(self):
        """
        _create_request() should create a POST request which includes a 'year' form variable.
        """
        year = 2000
        req = scraper._create_request(year=year, url=LOCAL_URL)
        assert "year" in req.data
        assert req.data["year"] == year
