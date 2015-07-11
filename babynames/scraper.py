from requests import Request


def get(year):
    pass


def _create_request(year, url, top=1000):
    """
    Creates a request to the URL with the necessary form parameters.
    """
    return Request("POST", url, data={"year": year, "top": top})
