from requests import Request, Session
from bs4 import BeautifulSoup


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
