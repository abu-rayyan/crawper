import logging
from threading import Thread
from src.r_engine.rengine import REngine

logger = logging.getLogger(__name__)


class AnalysisWorker(Thread):
    def __init__(self, queue):
        logger.debug('starting AnalysisWorker')
        Thread.__init__(self)
        self.queue = queue
        self.r_engine = REngine()

    def run(self):
        logger.debug('AnalysisWorker started')
        while True:
            product_asin = self.queue.get()
            self.r_engine.analyze_product(product_asin)
            self.queue.task_done()
