import logging

from src.common.db.postgres_pool import PgPool
from config.config import QUERIES

logger = logging.getLogger(__name__)


class AEngine:
    def __init__(self):
        logger.debug('initiating AEngine')
        self.pg_pool = PgPool()
