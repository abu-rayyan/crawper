import logging
import ConfigParser

from src.common import common
from src.common.thread import Worker
from src.common.config.urls import *
from Queue import Queue
from src.crawler import Crawler
from src.scraper import Scraper
from src.common.proxy_rotator import ProxyRotator

from src.common.db.postgres_pool import PgPool
from src.analysis_engine.aengine import AEngine

logger = logging.getLogger(__name__)


# start threaded version of crawper for new releases
def start_crawper(new_releases=False, best_sellers=False):
    logger.info('starting crawper')
    queue = Queue()

    if new_releases is True:
        logger.info('starting worker threads for New Releases')
        for work in range(len(NewReleases)):
            worker = Worker(queue)
            logger.debug('starting worker {index} @ {worker}'.format(index=work, worker=worker))
            worker.daemon = True
            worker.start()

        logger.info('sending data to workers')
        for link in NewReleases.values():
            queue.put(link)

        queue.join()

    if best_sellers is True:
        logger.info('starting worker threads for Best Sellers')
        for work in range(len(BestSellers)):
            worker = Worker(queue)
            logger.debug('starting worker {index} @ {worker}'.format(index=work, worker=worker))
            worker.daemon = True
            worker.start()

        logger.info('sending data to workers')
        for link in BestSellers.values():
            queue.put(link)

        queue.join()

def dev_tests():
    logger.info('Dev Testing started')
    asin = "B075R4B6DX"
    ae = AEngine()
    ae.get_product_reviews_from_db(asin)


def normal_mode_test():
    c = Crawler()
    links, file_ = c.get_product_links(NewReleases["SportsOutdoors"])
    s = Scraper()
    print(s.get_products_info(links, file_))


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

    #start_crawper(new_releases=True, best_sellers=False)
    #normal_mode_test()
    dev_tests()

    logger.info('closing database connection')
    db_conn.close_pool()


if __name__ == "__main__":
    main()
