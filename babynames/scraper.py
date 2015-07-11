from requests import Request, Session
from bs4 import BeautifulSoup
import re


def get(year):
    pass


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
    raise ValueError("Unable to find the names table in the given BeautifulSoup object")
