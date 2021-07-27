
import typing
import urllib.parse

import bs4
import loguru
import requests


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "uri_validator",
    "fetch_page_as_soup",
]


# See: https://stackoverflow.com/a/38020041/408734
def uri_validator(x: typing.Any) -> bool:
    """
    Checks whether an input parameter is a valid URI.
    """
    
    try:
        result = urllib.parse.urlparse(x)
        return all([
            result.scheme,
            result.scheme in ["file", "http", "https"],
            result.netloc,
        ])
    except:
        return False


def fetch_page_as_soup(
    url: str,
    silent_fail: bool = True,
) -> bs4.BeautifulSoup:
    """
    Fetches a provided URI and attempts to parse it using the BeautifulSoup
    package. By default, returns `None` if there are any issues; if the input
    parameter :py:
    """
    
    # some light validation
    
    if url is None:
        loguru.logger.error("no URL provided!")
        return
    
    if not uri_validator(url):
        loguru.logger.error("invalid URL provided!")
        return
    
    # make the request
    
    try:
        req = requests.get(url)
    except Exception as exc:
        # if not silent, then reraise exception
        if not silent_fail:
            raise exc
        
        # otherwise just log and return None
        loguru.logger.error("when fetching URL: ", url)
        loguru.logger.exception(exc)
        return
    
    # check request is valid
    
    if not req.ok:
        loguru.logger.warning("status code:", req.status_code)
        return
    
    # return beautiful soup
    
    content = req.content
    
    try:
        soup = bs4.BeautifulSoup(content, features="html.parser")
    except Exception as exc:
        # if not silent, then reraise exception
        if not silent_fail:
            raise exc
        
        # otherwise just log and return None
        loguru.logger.error("when parsing content of: ", url)
        loguru.logger.exception(exc)
        return
    
    return soup
