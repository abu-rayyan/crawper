from threading import Thread

from ..scraper import *

logger = logging.getLogger(__name__)


# ReviewWorker Threader
# TODO: Uncomplete
class ReviewWorker(Thread):
    def __init__(self, in_queue, res_queue):
        logger.debug('starting ReviewWorker')
        Thread.__init__(self)
        logger.debug('initializing ReviewWorker Queues')
        self.input_queue = in_queue
        self.response_queue = res_queue
        logger.debug('initializing scraper')
        self.scraper = Scraper()

    def run(self):
        logger.debug('ReviewWorker started')
        while True:
            page_link = self.input_queue.get()
            review_dict = self.scraper.scrap_review(page_link)
            self.response_queue.put(review_dict)
