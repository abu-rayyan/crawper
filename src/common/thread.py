import logging

from threading import Thread
from src.scraper import Scraper
from src.crawler import Crawler

logger = logging.getLogger(__name__)


# Main worker thread used in category wise threading
class Worker(Thread):
    def __init__(self, queue):
        logger.debug('starting Worker')
        Thread.__init__(self)
        logger.debug('initializing queue')
        self.queue = queue
        self.crawler = Crawler()
        self.scraper = Scraper()

# over-ridden run method as per requirements
    def run(self):
        logger.debug('worker started')
        while True:
            link = self.queue.get()
            logger.debug('link to crawl @ {link}'.format(link=link))
            links, file_name = self.crawler.get_product_links(link)

            logger.debug('links @ {links} file name @ {file}'.format(links=type(links), file=file_name))
            logger.debug('starting scraper')

            for link in links:
                self.scraper.get_products_info(link, file_name)

            self.queue.task_done()
