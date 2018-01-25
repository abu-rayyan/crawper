import logging

from config.config import *
from src.common import common
from src.common.db.postgres_pool import PgPool

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self):
        logger.info('initiating scrapper')
        self.base_url = URLS["BaseUrl"]
        self.pg_pool = PgPool()

    # scrap all products info based on links
    def get_products_info(self, links, category_name):
        """
        Scraps all products information
        :param links:
        :param category_name:
        """
        logger.info('scraping products info')

        product = {
            "Title": None,
            "Price": None,
            "ASIN": None,
            "TotalReviews": None,
            "ReviewsURL": None,
            "ProductLink": None,
            "ImageLink": None,
            "Reviews": None,
            "Rating": None
        }

        logger.debug('Product Dict: {prod}'.format(prod=product))

        for link in links:
            logger.debug('fetching product info @ {link}'.format(link=link))

            try:
                product["ASIN"] = link.split('/')[5]
                product["ProductLink"] = link
                logger.debug('ASIN: {asin}'.format(asin=product["ASIN"]))
            except Exception as e:
                logger.exception(e.message)

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

            try:
                image = web_page.find('div', {'id': 'imgTagWrapperId'}).find("img")
                product["ImageLink"] = image["data-a-dynamic-image"].split('{')[1].split('"')[1]
                logger.debug("Image Link: {link}".format(link=product["ImageLink"]))
            except Exception as e:
                product["ImageLink"] = None
                logger.exception(e.message)

            try:
                rating = web_page.find('i', {'class': 'a-icon a-icon-star-medium a-star-medium-4-5 averageStarRating'}).find("span")
                product["Rating"] = rating.text.split()[0]
                logger.debug("Product Rating: {rate}".format(rate=product["Rating"]))
            except Exception as e:
                logger.exception(e.message)

            self.insert_product_to_db(product, category_name)
            self.scrap_all_reviews(product)

    def scrap_all_reviews(self, product_dict):
        """
        Scrap reviews from reviews page
        :param product_dict: product data dictionary
        """
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
                    self.scrap_review(review_url, product_dict["ASIN"])

                next_link = next_page.find('li', {'class': 'a-last'})
                next_url = '{base_url}{url}'.format(base_url=self.base_url,
                                                    url=next_link.find('a').get('href').encode('utf-8'))
            except AttributeError as e:
                logger.exception('{exception}'.format(exception=e.message))
                break

    def scrap_review(self, review_url, product_asin):
        """
        Scraps a review
        :param review_url: url of the review page
        :param product_asin: asin number of the product
        :return:
        """
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
        self.insert_reviewer_to_db(review_dict)

    def insert_product_to_db(self, product, category_name):
        """
        Inserts product's data to the database
        :param product: product data dictionary
        :param category_name: category name of the product
        :return: bool
        """
        logger.debug('inserting product info to database')
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        insert_query = QUERIES["InsertProduct"]
        query_params = (product["ASIN"], product["Title"], product["Price"], product["ReviewsURL"],
                        category_name, product["ProductLink"], product["TotalReviews"], '0', product["ImageLink"],
                        product["Rating"])

        try:
            self.pg_pool.execute_query(pg_cursor, insert_query, query_params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    def insert_review_to_db(self, review, product_asin):
        """
        Insertes review data to the database
        :param review: review dictionary
        :param product_asin: asin no of the product
        :return: bool
        """
        logger.debug('inseritng review into the database')
        pg_conn, pg_cursor = self.pg_pool.get_conn()
        insert_query = QUERIES["InsertReview"]

        logger.debug('insert query: {query}'.format(query=insert_query))

        try:
            self.pg_pool.execute_query(pg_cursor, insert_query, (review["ReviewLink"], product_asin,
                                                                 review["ReviewTitle"], review["ReviewText"],
                                                                 review["ReviewerId"], review["ReviewDate"],
                                                                 review["ReviewRate"]))
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False

    def exists_product(self, asin_no):
        """
        Checks if a product exists in the database
        :param asin_no: asin number of the product
        :return: bool
        """
        logger.debug('checking if product {asin} exists in database'.format(asin=asin_no))

        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["ProductExists"]
        params = (asin_no,)

        try:
            if self.pg_pool.execute_query(pg_cursor, query, params)[0][0]:
                logger.debug('product {asin} exists in DB'.format(asin=asin_no))
                self.pg_pool.commit_changes(pg_conn)
                self.pg_pool.put_conn(pg_conn)
                return True
            else:
                logger.debug('product {asin} does not exists in DB'.format(asin=asin_no))
                self.pg_pool.put_conn(pg_conn)
                return False
        except Exception as e:
            logger.exception(e.message)
            self.pg_pool.put_conn(pg_conn)
            return None

    def insert_reviewer_to_db(self, review):
        logger.debug('inserting reviewer {name} information into database'.format(name=review["ReviewerName"]))

        pg_conn, pg_cursor = self.pg_pool.get_conn()
        query = QUERIES["InsertReviewer"]
        params = (review["ReviewerId"], review["ReviewerName"], review["ReviewerProfile"], 0, 0.0)

        try:
            self.pg_pool.execute_query(pg_cursor, query, params)
            self.pg_pool.commit_changes(pg_conn)
            self.pg_pool.put_conn(pg_conn)
            return True
        except Exception as e:
            logger.exception(e.message)
            return False
