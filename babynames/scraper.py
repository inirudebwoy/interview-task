from requests import Request


def get(year):
    pass


def _create_request(year, url):
    """
    Creates a request to the URL with the necessary form parameters.
    """
    return Request("POST", url, data={"year": year})
