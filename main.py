import logging
import ConfigParser
import threading

from src.common import common
from src.r_engine.utility import UtilityFunctions
from src.common.thread import Worker
from src.r_engine.threader.thread import AnalysisWorker
from src.common.config.urls import *
from Queue import Queue
from src.common.proxy_rotator import ProxyRotator
from src.r_engine.rengine import REngine

from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)


# start threaded version of crawper for new releases
def start_crawper():
    print('* starting crawper')
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


def start_rengine(db_pool):
    logger.info('starting threaded REngine')
    print('* starting REngine')

    queue = Queue()
    pg_conn, pg_cursor = db_pool.get_conn()
    utils = UtilityFunctions(pg_conn, pg_cursor, db_pool)

    asins = utils.get_zero_rank_asins_from_db()
    db_pool.commit_changes(pg_conn)
    db_pool.put_conn(pg_conn)

    MAX_THREADS = 99

    while MAX_THREADS is not 0:
        for work in range(MAX_THREADS):
            worker = AnalysisWorker(queue)
            logger.debug('started AnalysisWorker {w} @ {id}'.format(w=work, id=worker))
            worker.daemon = True
            worker.start()

        for asin in asins:
            queue.put(asins.pop()[0])
        queue.join()

        if len(asins) < MAX_THREADS:
            MAX_THREADS = len(asins)
        else:
            continue


def main():
    logger.info('checking configs')
    print('* checking configs')
    if not common.exists_dir("temp"):
        common.make_dir("temp")

    print('* loading project configs')
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    # logging.basicConfig(filename='logs.log', level=logging.getLevelName(config.get('App', 'Mode')))
    logging.basicConfig(level=logging.getLevelName(config.get('App', 'Mode')))

    db_conn_params = {
        "Host": config.get('Database', 'Host'),
        "Port": config.get('Database', 'Port'),
        "Database": config.get('Database', 'Database'),
        "User": config.get('Database', 'User'),
        "Password": config.get('Database', 'Password')
    }

    logger.info('connecting to database')
    print('* connecting to database')
    db_conn = PgPool()  # TODO: Replace if found better way for singleton mem sharing
    db_conn.create_pool(db_conn_params)

    logger.info('assembling proxy rotator')

    # TODO: Replace if found a better way of sharing same mem space
    # noinspection PyUnusedLocal
    rotator = ProxyRotator('assets/Proxies.txt')  # used as singleton obj

    start_crawper()
    start_rengine(db_conn)
    logger.info('closing database connection')
    print('* closing database pool')
    db_conn.close_pool()


if __name__ == "__main__":
    main()
