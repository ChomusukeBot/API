from urllib.parse import urlparse


def parse_url(url):
    """
    Parses the specified URL with urlparse and is returned without the path.
    """
    newurl = urlparse(url)
    return "{0}://{1}".format(newurl.scheme, newurl.netloc)
