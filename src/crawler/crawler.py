import logging

from config.config import *
from utils import Utils
from src.common import common
from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(self):
        logger.info('initiating crawler')
        self.base_url = URLS.get("BaseUrl")
        self.check_configs()
        self.pg_ = PgPool()
        self.utils = Utils()

    # checks basic configs of crawler
    @staticmethod
    def check_configs():
        logger.debug('checking crawler configs')

        if not common.exists_dir('temp/crawler'):
            common.make_dir('temp/crawler')
        else:
            logger.debug('crawler dir [/temp/crawler/] exists')

    # get product category name from url
    @staticmethod
    def get_category(url):  # TODO: Replace with category name from thread
        logger.debug('getting category name @ {url}'.format(url=url))
        category = url.split('/')
        logger.debug('category: {category}'.format(category=category[-2]))
        return category[-2]

    # get sports/outdoors products links (all 5 tabs)
    def get_product_links(self, url):
        category_id = self.get_category(url)
        logger.debug('products category name: {file}'.format(file=category_id))

        if not self.utils.exists_category_in_db(category_id):
            if self.utils.insert_category_into_db(category_id):
                logger.debug('inserted category {id} into database'.format(id=category_id))
            else:
                logger.error('category {id} insertion into database failed'.format(id=category_id))

        product_urls = self.find_urls(url, category_id)
        return product_urls, category_id

    # TODO: Remove & Relace hard-coded tab entries with generics
    def find_urls(self, url, category_id):
        """
        Finds urls of products in all 5 tabs
        :param category_id: id of category
        :param url: url of the main page
        :return: products link
        """
        logger.info("fetching product links")
        product_links = []
        tab = 1

        while tab < 6:
            link_url = "{url}#{tab}".format(url=url, tab=tab)
            logger.debug('current page url: {url}'.format(url=link_url))
            soup = common.request_page(link_url)
            links = soup.find_all('a', {'class': 'a-link-normal'})
            logger.debug('fetching links with attribute [class=a-link-normal]')

            try:
                for link in links:
                    product_link = link.get('href')
                    if product_link.startswith('/') and not product_link.startswith('/product-reviews'):
                        prod_link = '{base_url}{link}'.format(base_url=self.base_url, link=product_link)
                        splitted_link = prod_link.split('/')
                        if category_id in splitted_link[6]:
                            product_asin = splitted_link[5]

                            if not self.utils.exists_product_in_db(product_asin):
                                logger.debug('product does not exists in the database')
                                product_links.append(prod_link.encode('utf-8'))
                            else:
                                logger.debug('product exists in the database')
                    else:
                        continue
            except Exception as e:
                logger.exception(e.message)
            tab += 1
        return product_links
