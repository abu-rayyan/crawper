import requests
import time
import os
import logging

from bs4 import BeautifulSoup
from random import randint
from fake_useragent import UserAgent
from src.common.proxy_rotator import ProxyRotator

logger = logging.getLogger(__name__)


# Common functions used in the app
# TODO: Adopt OO Paradigm here

# noinspection SpellCheckingInspection
def request_page(page_url):
    """
    Sends get request and return page
    :param page_url: web-page url
    :type page_url: str
    :return: bs4 type object
    """
    rotator = ProxyRotator()

    logger.info('requesting page @ {url}'.format(url=page_url))
    sleep_time = randint(1, 5)
    user_agent = UserAgent()
    logger.debug('fake_useragent initialized: {addr}'.format(addr=user_agent))
    time.sleep(sleep_time)
    headers = {'User-Agent': str(user_agent.random)}
    logger.debug('Headers: {head}'.format(head=headers))

    try:
        response = requests.get(page_url, headers=headers, proxies=rotator.get_proxy())
        logger.debug('requests response @ {res}'.format(res=response))
        page_content = BeautifulSoup(response.content, 'lxml')
        logger.debug('bs4 page content @ {content}'.format(content=type(page_content)))
        return page_content
    except requests.exceptions.RequestException as e:
        logger.exception('{exception}'.format(exception=e))


def make_dir(dir_path):
    """
    Create a new directory

    :param dir_path: path to the dir
    :type dir_path: str
    """
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except OSError as e:
        logger.exception('{exception}'.format(exception=e.message))


# checks if a particular dir exists
def exists_dir(dir_path):
    return os.path.isdir(dir_path)


# checks if a particular file exists
def exists_file(file_path):
    return os.path.isfile(file_path)


# return creation time of file (depreciated)
# TODO: Remove if not needed any more
def get_creation_time(file_path):
    return os.path.getctime(file_path)


# return current system time (depreciated)
# TODO: Remove if not needed any more
def get_current_time():
    return time.time()
