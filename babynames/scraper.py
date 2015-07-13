from requests import Request, Session
from bs4 import BeautifulSoup
import re


class NoNamesTableError(Exception):
    pass


class IncorrectAmountOfTDElementsError(Exception):
    pass


class TDElementsOutOfOrderError(Exception):
    pass


def get(year, url):
    """
    Performs a request to the URL provided, parses the response and returns a tuple containing
    two dictionaries - one for boys and one for girls names. The dictionaries have the name as the
    key and the rank as the value.
    """
    req = _create_request(year, url)
    resp = _perform_request(req)
    bs = _parse_response(resp)
    names = _extract_names_table(bs)
    boys, girls = {}, {}
    for tr in _extract_name_rows(names):
        rank, boy, girl = _extract_names_from_row(tr)
        boys[boy] = rank
        girls[girl] = rank
    return boys, girls


def _create_request(year, url, top=1000):
    """
    Creates a request to the URL with the necessary form parameters.
    """
    return Request("POST", url, data={"year": year, "top": top})


def _perform_request(req):
    """
    Perform the request and return a Response.
    """
    s = Session()
    return s.send(s.prepare_request(req))


def _parse_response(resp):
    """
    Parses the response into a BeautifulSoup object.
    """
    return BeautifulSoup(resp.text)


def _extract_names_table(bs):
    """
    Returns the names table from the given BeautifulSoup object.
    """
    for table in bs.findAll("table"):
        if re.match(r"^Popularity for top \d+$", table.attrs.get("summary", "")):
            return table
    raise NoNamesTableError("Unable to find the names table in the given BeautifulSoup object")


def _extract_name_rows(table):
    """
    Removes the first and last tr from the table and returns a list of trs.
    """
    return table.findAll("tr")[1:-1]


def _extract_names_from_row(tr):
    """
    Returns a tuple containing the boy's and girl's name as separate elements
    when given a BeautifulSoup tr in the correct format.

    eg. '<tr align="right"><td>786</td><td>Ellis</td><td>Kaylah</td></tr>'
    """
    tds = tr.findAll("td")
    if len(tds) != 3:
        raise IncorrectAmountOfTDElementsError(
            "Expecting the tr to contain three td elements but it contained %s" % len(tds))
    try:
        rank = int(tds[0].text)
    except ValueError:
        raise TDElementsOutOfOrderError(
            "The first td element was not a rank number: %s" % tds[0].text)
    names = tuple([t.text for t in tds][1:])
    for name in names:
        try:
            int(name)
        except ValueError:
            # Good, it's not a number!
            continue
        raise TDElementsOutOfOrderError(
            "TD elements must have been in the wrong order as '%s' is not any name I've heard of"
            % name)
    return (rank,) + names
