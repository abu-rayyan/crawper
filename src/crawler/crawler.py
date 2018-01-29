import logging

from config.config import *
from src.common import common
from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(self):
        logger.info('initiating crawler')
        self.base_url = URLS.get("BaseUrl")
        self.check_configs()
        self.pg_ = PgPool()

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
        category_name = self.get_category(url)
        logger.debug('products category name: {file}'.format(file=category_name))

        if not self.exists_category(category_name):
            self.insert_category(category_name)

        product_urls = self.find_urls(url, category_name)
        return product_urls, category_name

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
                            print(prod_link)
                            product_asin = splitted_link[5]

                            if not self.exists_product(product_asin):
                                product_links.append(prod_link.encode('utf-8'))
                    else:
                        continue
            except Exception as e:
                logger.exception(e.message)
            tab += 1
        return product_links

    def exists_product(self, product_asin):
        """
        Checks if a product exists in the database
        :param product_asin: asin of product
        :return: bool
        """
        pg_conn, pg_cursor = self.pg_.get_conn()
        logger.debug('checking if product {asin} exists in database'.format(asin=product_asin))
        query = QUERIES["ExistsProduct"]
        params = (product_asin,)

        try:
            success_bool = self.pg_.execute_query(pg_cursor, query, params)
            logger.debug('product {asin} exists in database'.format(asin=product_asin))
            self.pg_.put_conn(pg_conn)
            return success_bool[0][0]
        except Exception as e:
            logger.exception(e.message)
            self.pg_.put_conn(pg_conn)
            return None

    def exists_category(self, category_name):
        """
        Checks if a particular category exists in database
        :param category_name: category name (str)
        :return: bool
        """
        logger.debug('checking if category {name} exists in database'.format(name=category_name))
        pg_conn, pg_cursor = self.pg_.get_conn()
        query = QUERIES["ExistsCategory"]
        params = (category_name,)

        try:
            if self.pg_.execute_query(pg_cursor, query, params)[0][0]:
                logger.debug('category {name} exists in the database'.format(name=category_name))
                self.pg_.put_conn(pg_conn)
                return True
            else:
                logger.debug('category {name} does not exists in database')
                self.pg_.put_conn(pg_conn)
                return False
        except Exception as e:
            logger.exception(e.message)
            self.pg_.put_conn(pg_conn)
            return None

    def insert_category(self, category_name):
        """
        Inserts a new category into the DB
        :param category_name: name of the category
        :return: bool
        """
        logger.debug('inserting new category {name} into the database'.format(name=category_name))
        pg_conn, pg_cursor = self.pg_.get_conn()
        query = QUERIES["InsertCategory"]
        params = (category_name,)

        try:
            self.pg_.execute_query(pg_cursor, query, params)
            self.pg_.commit_changes(pg_conn)
            self.pg_.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            self.pg_.put_conn(pg_conn)
            return False

    def get_links_from_db(self, category_name):
        """
        Get links of products for existing category in DB
        :param category_name: name of the category
        :return: product links
        """
        logger.debug('getting product links from database')
        pg_conn, pg_cursor = self.pg_.get_conn()
        query = QUERIES["SelectProductLink"]
        params = (category_name,)

        try:
            query_responce = self.pg_.execute_query(pg_cursor, query, params)
            product_links = [link[0] for link in query_responce]
            self.pg_.commit_changes(pg_conn)
            self.pg_.put_conn(pg_conn)
            return product_links
        except Exception as e:
            logger.exception(e.message)
            return None
