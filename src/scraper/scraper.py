import json
import logging

from psycopg2 import sql
from config.config import *
from src.common import common
from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self):
        logger.info('initiating scrapper')
        self.base_url = URLS["BaseUrl"]
        self.pg_pool = PgPool()
        self.check_configs()

    # checks basic configs of scraper
    @staticmethod
    def check_configs():
        logger.debug('checking scraper configurations')

        logger.debug('checking if temp/scraper exists')
        if not common.exists_dir('temp/scraper'):
            logger.debug('temp/scraper does not exists, creating new')
            common.make_dir('temp/scraper')
        else:
            logger.debug('temp/scraper exists')

    # scrap all products info based on links
    # TODO: add db operations instead of filing
    def get_products_info(self, links, category_name):
        logger.info('scraping products info')

        logger.debug('checking if temp/scraper/{file}.json exists'.format(file=category_name))
        if not common.exists_file('temp/scraper/{file}.json'.format(file=category_name)):
            logger.debug('temp/scraper/{file}.json does not exists, creating new'.format(file=category_name))
            products_file = open('temp/scraper/{file}.json'.format(file=category_name), 'w')
        else:
            logger.debug('temp/scraper/{file}.json exists, opening file'.format(file=category_name))
            products_file = open('temp/scraper/{file}.json'.format(file=category_name), 'a')

        products = {}
        product = {
            "Title": None,
            "Price": None,
            "ASIN": None,
            "TotalReviews": None,
            "ReviewsURL": None,
            "ProductLink": None,
            "Reviews": None
        }

        logger.debug('Products Dict: {prods}   Product Dict: {prod}'.format(prods=products, prod=product))

        for link in links:
            logger.debug('fetching product info @ {link}'.format(link=link))
            web_page = common.request_page(link)

            try:
                price = web_page.find('span', {'id': 'priceblock_ourprice'})
                product["Price"] = price.text.encode('utf-8')
                logger.debug("Price: {price}".format(price=price.text))
            except Exception as e:
                product["Price"] = None
                logger.exception('{exception}'.format(exception=e.message))

            try:
                title = web_page.find('span', {'id': 'productTitle'})
                label = ' '.join(title.text.split())
                product["Title"] = label.encode('utf-8')
                logger.debug("Title: {title}".format(title=label))
            except Exception as e:
                product["Title"] = None
                logger.exception('{exception}'.format(exception=e.message))

            try:
                reviews_url = web_page.find('a', {'id': 'dp-summary-see-all-reviews'})
                product["ReviewsURL"] = "{base}{url}".format(base=self.base_url,
                                                             url=reviews_url.get('href').encode('utf-8'))
                logger.debug("Review URL: {url}".format(url=reviews_url.get('href').encode('utf-8')))
            except Exception as e:
                product["ReviewsURL"] = None
                logger.exception('{exception}'.format(exception=e.message))

            try:
                total_reviews = web_page.find('span', {'class': 'a-size-medium totalReviewCount'})
                product["TotalReviews"] = total_reviews.text.encode('utf-8')
                logger.debug("Total Reviews: {rev}".format(rev=total_reviews.text))
            except Exception as e:
                product["TotalReviews"] = None
                logger.exception('{exception}'.format(exception=e.message))

            asin = link.split('/')
            product["ASIN"] = asin[5]
            product["ProductLink"] = link
            logger.debug("ASIN: {asin}".format(asin=asin[5]))
            self.insert_product_to_db(product, category_name)

            prod = self.scrap_all_reviews(product)
            logger.debug('updating products dict')
            products.update(prod)
            logger.debug('Product: {prod}'.format(prod=product))

        logger.debug('writing products information to file')
        products_file.write(json.dumps(products))
        products_file.write('\n\n')
        products_file.close()

        return products

    # find each review URL on review page
    def scrap_all_reviews(self, product_dict):
        logger.info("scraping reviews")
        next_url = product_dict["ReviewsURL"]
        logger.debug('Reviews URL: {url}'.format(url=next_url))
        global next_page

        while True:
            logger.debug('Next URL: {url}'.format(url=next_url))
            try:
                next_page = common.request_page(next_url)
                review_links = next_page.find_all('a', {
                    'class': 'a-size-base a-link-normal review-title a-color-base a-text-bold'})

                for link in review_links:
                    review_url = '{base_url}{url}'.format(base_url=self.base_url, url=link.get('href').encode('utf-8'))
                    logger.debug('review url: {url}'.format(url=review_url))
                    product_dict["Reviews"] = self.scrap_review(review_url, product_dict["ASIN"])

                next_link = next_page.find('li', {'class': 'a-last'})
                next_url = '{base_url}{url}'.format(base_url=self.base_url,
                                                    url=next_link.find('a').get('href').encode('utf-8'))
            except AttributeError as e:
                logger.exception('{exception}'.format(exception=e.message))
                break
        logger.debug('product dict: {dict}'.format(dict=product_dict))
        return product_dict

    # scrap a single review by review url
    def scrap_review(self, review_url, product_asin):
        logger.info("scraping review @ {url}".format(url=review_url))
        global soup

        review_dict = {
            "ReviewTitle": None,
            "ReviewLink": review_url,
            "ReviewerName": None,
            "ReviewerProfile": None,
            "ReviewerId": None,
            "ReviewDate": None,
            "ReviewText": None,
            "ReviewRate": None,
            "TotalComments": None,
            "Comments": None,
            "Profile": None
        }
        logger.debug('review dict: {dict}'.format(dict=review_dict))

        if review_url is not None:
            logger.debug('scrapping review @ {url}'.format(url=review_url))
            soup = common.request_page(review_url)

            try:
                review_title = soup.find('a',
                                         {'class': 'a-size-base a-link-normal review-title a-color-base a-text-bold'})
                review_dict["ReviewTitle"] = review_title.text.encode('utf-8')
                logger.debug('review title: {title}'.format(title=review_dict["ReviewTitle"]))
            except Exception as e:
                review_dict["ReviewTitle"] = None
                logger.exception('{exception}'.format(exception=e.message))

            try:
                author_name = soup.find('a', {'class': 'a-size-base a-link-normal author'})
                review_dict["ReviewerName"] = author_name.text.encode('utf-8')
                review_dict["ReviewerProfile"] = '{base_url}{profile}'.format(base_url=self.base_url,
                                                                              profile=author_name.get('href').encode(
                                                                                  'utf-8'))
                review_dict["ReviewerId"] = review_dict["ReviewerProfile"].split('/')[5]

                logger.debug('Reviewer Name: {name}'.format(name=review_dict["ReviewerName"]))
                logger.debug('Reviewer Profile: {link}'.format(link=review_dict["ReviewerProfile"]))
                logger.debug('Reviewer ID: {id}'.format(id=review_dict["ReviewerId"]))
            except Exception as e:
                review_dict["ReviewerName"] = None
                review_dict["ReviewerProfile"] = None
                review_dict["ReviewerId"] = None
                logger.exception('{exception}'.format(exception=e.message))

            try:
                review_time = soup.find('span', {'class': 'a-size-base a-color-secondary review-date'})
                date = review_time.text
                review_dict["ReviewDate"] = date[3:]
                logger.debug('Review Date: {date}'.format(date=review_dict["ReviewDate"]))
            except Exception as e:
                review_dict["ReviewDate"] = None
                logger.exception('{exception}'.format(exception=e.message))

            try:
                review_text = soup.find('span', {'class': 'a-size-base review-text'})
                review_dict["ReviewText"] = review_text.text.encode('utf-8')
                logger.debug('Review Text: {text}'.format(text=review_dict["ReviewText"]))
            except Exception as e:
                review_dict["ReviewText"] = None
                logger.exception('{exception}'.format(exception=e.message))

            try:
                review_rate = soup.find('span', {'class': 'a-icon-alt'})
                rate = review_rate.text.split()
                review_dict["ReviewRate"] = rate[0].encode('utf-8')
                logger.debug('Review Rate: {rate}'.format(rate=review_dict["ReviewRate"]))
            except Exception as e:
                review_dict["ReviewRate"] = None
                logger.exception('{exception}'.format(exception=e.message))
        logger.debug('Review: {dict}'.format(dict=review_dict))
        self.insert_review_to_db(review_dict, product_asin)

        return review_dict

    # insert product info into the database
    def insert_product_to_db(self, product, category_name):
        logger.debug('inserting product info to database')
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        insert_query = QUERIES["InsertProduct"]
        query_params = (product["ASIN"], product["Title"], product["Price"], product["ReviewsURL"],
                        category_name, product["ProductLink"],  product["TotalReviews"])

        try:
            self.pg_pool.execute_query(pg_cursor, insert_query, query_params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    # insert product review into database
    def insert_review_to_db(self, review, product_asin):
        logger.debug('inseritng review into the database')
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        insert_query = QUERIES["InsertReview"]

        logger.debug('insert query: {query}'.format(query=insert_query))

        try:
            self.pg_pool.execute_query(pg_cursor, insert_query, (review["ReviewLink"], product_asin, review["ReviewTitle"], review["ReviewText"], review["ReviewRate"], review["ReviewerId"], review["ReviewDate"]))
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False
