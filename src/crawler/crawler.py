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
        self.pg_pool = PgPool()
        self.pg_conn, self.pg_cursor = self.pg_pool.get_conn()
        self.utils = Utils(self.pg_conn, self.pg_cursor, self.pg_pool)

    def put_db_connection_back(self):
        logger.debug('putting database connection back into pool')
        self.pg_pool.commit_changes(self.pg_conn)
        self.pg_pool.put_conn(self.pg_conn)

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

    def validate_product(self, product_asin):
        logger.debug('checking if product {asin} validates for being scraped'.format(asin=product_asin))
        global validate_bool
        try:
            exists = self.utils.exists_product_in_db(product_asin)
            if exists is not None:
                if exists:
                    logger.debug('product {asin} exists in database'.format(asin=product_asin))
                    total_reviews = self.utils.get_total_reviews_from_db(product_asin).replace(',', '')
                    scraped_reviews = self.utils.get_no_of_scraped_reviews_from_db(product_asin)
                    global percent_scraped_reviews
                    if total_reviews is not None & scraped_reviews is not None:
                        if not total_reviews == 0:
                            percent_scraped_reviews = (float(scraped_reviews) / float(total_reviews)) * 100

                    if 0 <= int(total_reviews) <= 100:
                        logger.debug('checking if scraped reviews are more then 90%')
                        if percent_scraped_reviews >= 90:
                            logger.debug('scraped reviews >= 90% True')
                            validate_bool = False
                        else:
                            logger.debug('scraped reviews >= 90% False')
                            validate_bool = True
                    elif 101 <= int(total_reviews) <= 1000:
                        logger.debug('checking if scraped reviews are more then 50%')
                        if percent_scraped_reviews >= 50:
                            logger.debug('scraped reviews >= 50% True')
                            validate_bool = False
                        else:
                            logger.debug('scraped reviews >= 50% False')
                            validate_bool = True
                    elif 1001 <= int(total_reviews) <= 5000:
                        logger.debug('checking if scraped reviews are more then 25%')
                        if percent_scraped_reviews >= 25:
                            logger.debug('scraped reviews >= 25% True')
                            validate_bool = False
                        else:
                            logger.debug('scraped reviews >= 25% False')
                            validate_bool = True
                    elif 5001 <= int(total_reviews) <= 10000:
                        logger.debug('checking if scraped reviews are more then 10%')
                        if percent_scraped_reviews >= 10:
                            logger.debug('scraped reviews >= 10% True')
                            validate_bool = False
                        else:
                            logger.debug('scraped reviews >= 10% False')
                            validate_bool = True
                    else:
                        logger.debug('checking if scraped reviews are more then 1%')
                        if percent_scraped_reviews >= 1:
                            logger.debug('scraped reviews >= 1% True')
                            validate_bool = False
                        else:
                            logger.debug('scraped reviews >= 1% False')
                            validate_bool = True
                else:
                    logger.debug('product does not exists in database')
                    validate_bool = True
            else:
                logger.error('something bad happened')
        except Exception as e:
            logger.exception(e.message)
        return validate_bool

    # get sports/outdoors products links (all 5 tabs)
    def get_product_links(self, url):
        print('* crawling products')
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
                            if self.validate_product(product_asin):
                                logger.debug('product {asin} needs to be scraped'.format(asin=product_asin))
                                product_links.append(prod_link.decode('utf-8'))
                            else:
                                logger.debug('product {asin} doesnot validated to be scraped')
                    else:
                        continue
            except Exception as e:
                logger.exception(e.message)
            tab += 1
        return product_links
