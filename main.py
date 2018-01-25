import logging
import ConfigParser

from src.common import common
from src.common.thread import Worker
from src.common.config.urls import *
from Queue import Queue
from src.common.proxy_rotator import ProxyRotator
from src.r_engine.rengine import REngine
from src.scraper import Scraper

from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)


# start threaded version of crawper for new releases
def start_crawper():
    logger.info('starting crawper')
    queue = Queue()

    for keys, links in Products.iteritems():
        logger.info('starting worker threads for {work}'.format(work=keys))
        for work in range(len(links)):
            worker = Worker(queue)
            logger.debug('starting worker {index} @ {worker}'.format(index=work, worker=worker))
            worker.daemon = True
            worker.start()

        logger.info('sending input data to workers')
        for key, link in links.iteritems():
            queue.put(link)
        queue.join()


def start_dev():
    logger.info('starting development mode')
    links = ['https://www.amazon.com/HotHands-Hand-Warmers-Pair-Value/dp/B07962763T/',
             'https://www.amazon.com/POY-Fitbit-Classic-Special-Replacement/dp/B076Z8S4V5/']
    sc = Scraper()
    sc.get_products_info(links, 'abc')


def main():
    logger.info('checking configs')
    if not common.exists_dir("temp"):
        common.make_dir("temp")

    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    logging.basicConfig(level=logging.getLevelName(config.get('App', 'Mode')))

    db_conn_params = {
        "Host": config.get('Database', 'Host'),
        "Port": config.get('Database', 'Port'),
        "Database": config.get('Database', 'Database'),
        "User": config.get('Database', 'User'),
        "Password": config.get('Database', 'Password')
    }

    logger.info('connecting to database')
    db_conn = PgPool()  # TODO: Replace if found better way for singleton mem sharing
    db_conn.create_pool(db_conn_params)

    logger.info('assembling proxy rotator')

    # TODO: Replace if found a better way of sharing same mem space
    # noinspection PyUnusedLocal
    rotator = ProxyRotator('temp/temp/Proxies.txt')  # used as singleton obj

    start_crawper()
    r_engine = REngine()
    r_engine.start_engine()
    start_dev()

    logger.info('closing database connection')
    db_conn.close_pool()


if __name__ == "__main__":
    main()
