import logging
import time
import ConfigParser

from src.common import common
from src.r_engine.rengine import REngine
from src.r_engine.utility import UtilityFunctions
from src.common.thread import Worker
from src.r_engine.threader.thread import AnalysisWorker
# from src.common.config.urls import *
from Queue import Queue
from src.common.proxy_rotator import ProxyRotator
from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)

# noinspection PyPep8Naming,SpellCheckingInspection
def start_crawper(threads, db_pool):
    """
    Starts threaded crawper
    :param threads: no of max threads
    """
    logger.info('starting crawler')
    queue = Queue()
    links_list = []
    pg_conn, pg_cursor = db_pool.get_conn()
    utils = UtilityFunctions(pg_conn, pg_cursor, db_pool)

    links = utils.get_url_from_categories()
    '''
    for keys, links in Products.iteritems():
        links_list.extend(links.values())
    '''
    for link in links:
        print link
        links_list.extend(link)

    MAX_THREADS = int(threads)
    while MAX_THREADS is not 0:
        for work in range(MAX_THREADS):
            worker = Worker(queue)
            logger.debug('starting worker {index} @ {worker}'.format(index=work, worker=worker))
            worker.daemon = True
            worker.start()

        logger.debug('sending input data to worker thread')
        # noinspection PyUnusedLocal
        for link in links_list:
            queue.put(links_list.pop())
        queue.join()

        if len(links_list) < MAX_THREADS:
            MAX_THREADS = len(links_list)
        else:
            continue


# noinspection PyPep8Naming,SpellCheckingInspection
def start_rengine(db_pool, threads):
    """
    Starts threaded REngine
    :param db_pool: database pool connection
    :param threads: no of max threads
    """
    logger.info('starting threaded REngine')
    print('* starting REngine')

    queue = Queue()
    pg_conn, pg_cursor = db_pool.get_conn()
    utils = UtilityFunctions(pg_conn, pg_cursor, db_pool)

    asins = utils.get_products_asin_from_db()
    #print(asins)
    db_pool.commit_changes(pg_conn)
    db_pool.put_conn(pg_conn)

    MAX_THREADS = int(threads)

    while MAX_THREADS is not 0:
        for work in range(MAX_THREADS):
            worker = AnalysisWorker(queue)
            logger.debug('started AnalysisWorker {w} @ {id}'.format(w=work, id=worker))
            worker.daemon = True
            worker.start()

        # noinspection PyUnusedLocal
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

    # TODO: Use logs file & Normal Mode when deployed in production
    # TODO: App Mode can be passed through args, use whatever is better
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
    # noinspection PyUnusedLocal,SpellCheckingInspection
    rotator = ProxyRotator('assets/Proxies.txt')  # used as singleton obj

    # noinspection SpellCheckingInspection
    # disable r_Engine
    rengine_threads = config.get('REngine', 'Max Threads')
    # noinspection SpellCheckingInspection
    crawper_threads = config.get('Crawper', 'Max Threads')

    start_crawper(crawper_threads, db_conn)
    #start_rengine(db_conn, rengine_threads)
    logger.info('closing database connection')
    print('* closing database pool')
    db_conn.close_pool()


if __name__ == "__main__":
    main()
