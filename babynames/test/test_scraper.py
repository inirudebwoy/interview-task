import os
import codecs
import pytest
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
        _parse_response() should return a BeautifulSoup object.
        """
        resp = Response()
        resp._content = self.example_html
        bs = scraper._parse_response(resp)
        assert isinstance(bs, BeautifulSoup)

    def test_extract_names_table_returns_table(self):
        """
        _extract_names_table() should return the correct BeautifulSoup table element.
        """
        resp = Response()
        resp._content = self.example_html
        bs = scraper._parse_response(resp)
        table = scraper._extract_names_table(bs)
        assert "summary" in table.attrs
        assert table.attrs["summary"] == "Popularity for top 1000"

    def test_extract_names_table_raises_exception_when_table_doesnt_exist(self):
        """
        _extract_names_table() should raise a NoNamesTableError if it can't find the names table.
        """
        with pytest.raises(scraper.NoNamesTableError):
            scraper._extract_names_table(BeautifulSoup())

    def test_extract_names_from_row(self):
        """
        _extract_names_from_row() should return a tuple of (<rank>, <boy_name>, <girl_name>) when
        given a BeautifulSoup 'tr' object.
        """
        tr_html = '<tr align="right"><td>786</td><td>Ellis</td><td>Kaylah</td></tr>'
        tr = BeautifulSoup(tr_html)
        rank, boy, girl = scraper._extract_names_from_row(tr)
        assert rank == 786
        assert boy == "Ellis"
        assert girl == "Kaylah"

    def test_extract_names_from_row_raises_exception_when_not_enough_tds(self):
        """
        _extract_names_from_row() should raise a IncorrectAmountOfTDElementsError if there are less
        than three td elements.
        """
        tr_html = '<tr align="right"><td>Ellis</td><td>Kaylah</td></tr>'
        tr = BeautifulSoup(tr_html)
        with pytest.raises(scraper.IncorrectAmountOfTDElementsError):
            scraper._extract_names_from_row(tr)

    def test_extract_names_from_row_raises_exception_when_too_many_tds(self):
        """
        _extract_names_from_row() should raise a IncorrectAmountOfTDElementsError if there are more
        than three td elements.
        """
        tr_html = '<tr align="right"><td>786</td><td>Ellis</td><td>Kaylah</td><td>foo</td></tr>'
        tr = BeautifulSoup(tr_html)
        with pytest.raises(scraper.IncorrectAmountOfTDElementsError):
            scraper._extract_names_from_row(tr)

    def test_extract_names_from_row_raises_exception_when_tds_are_out_of_order(self):
        """
        _extract_names_from_row() should raise a TDElementsOutOfOrderError if the tds are in a
        different order to what it expects and it would otherwise return a number as a name.
        """
        tr_html = '<tr align="right"><td>Ellis</td><td>786</td><td>Kaylah</td></tr>'
        tr = BeautifulSoup(tr_html)
        with pytest.raises(scraper.TDElementsOutOfOrderError):
            scraper._extract_names_from_row(tr)

    def test_get_returns_tuple_of_dicts_for_boy_and_girl(self):
        """
        get() should return a tuple containing a dictionary for boy's and girl's names
        respectively. The dicts should have the names as keys and their rank as values.
        """
        fake_resp = Response()
        fake_resp._content = self.example_html
        with patch.object(Session, "send", return_value=fake_resp):
            boys, girls = scraper.get(year=2000, url=LOCAL_URL)
        assert isinstance(boys, dict)
        assert isinstance(girls, dict)
        assert "Ellis" in boys
        assert "Yolanda" in girls
        assert boys["Ellis"] == 786
        assert girls["Yolanda"] == 780

    def test_extract_name_rows(self):
        """
        _extract_name_rows() should return only the name trs from the given table. Essentially
        just removing the first and last trs.
        """
        html = """
        <html>
         <body>
          <table>
           <tr><th>This is a header row</th></tr>
           <tr><td>1</td><td>Ellis</td><td>Sarah</td></tr>
           <tr><td>2</td><td>Michal</td><td>Lucy</td></tr>
           <tr><td>This is a footer row</td></tr>
          </table>
         </body>
        </html>
        """
        table = BeautifulSoup(html)
        rows = scraper._extract_name_rows(table)
        assert len(rows) == 2
        for row in rows:
            assert not any(("header row" in row.text, "footer row" in row.text))
