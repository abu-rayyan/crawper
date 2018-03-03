import logging
import threading
from threading import Thread
from src.r_engine.rengine import REngine

logger = logging.getLogger(__name__)
MAX_THREADS = 100
thread_limiter = threading.BoundedSemaphore(MAX_THREADS)


# noinspection SpellCheckingInspection
class AnalysisWorker(Thread):
    def __init__(self, queue):
        logger.debug('starting AnalysisWorker')
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        logger.debug('AnalysisWorker started')
        while True:
            product_asin = self.queue.get()
            r_engine = REngine()
            r_engine.start_engine()
            r_engine.analyze_product(product_asin)
            r_engine.generate_product_triggers(product_asin)
            r_engine.put_db_connection_back()
            self.queue.task_done()
