import logging
from threading import Thread
from src.crawler import Crawler

logger = logging.getLogger(__name__)


# LinksWorker thread
# TODO: Improve it to run inside parent threads
class LinksWorker(Thread):
    def __init__(self, queue, res_queue):
        logger.debug('starting Links Worker')
        Thread.__init__(self)
        logger.debug('initializing LinksWorker queue')
        self.queue = queue
        self.response_queue = res_queue
        logger.debug('initializing crawler')
        self.crawler = Crawler()

    # over-ridden run method as per requirements
    def run(self):
        logger.debug('LinksWorker started')
        while True:
            page_link = self.queue.get()
            urls = self.crawler.get_product_links(page_link)
            self.response_queue.put(urls)
            self.queue.task_done()
