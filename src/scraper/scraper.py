import logging
import datetime
from config.config import *
from src.common import common
from utils import Utils

logger = logging.getLogger(__name__)


# noinspection SpellCheckingInspection
class Scraper:
    def __init__(self):
        logger.info('initiating scrapper')
        print('* scraping products')
        self.base_url = URLS["BaseUrl"]
        self.utils = Utils()

    def get_products_info(self, link, category_name):
        """
        Scraps all products information
        :param link:
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
            "Rating": None,
            "TodayDate": None
        }

        logger.debug('Product Dict: {prod}'.format(prod=product))

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
            rating = web_page.find('i',
                                   {'class': 'a-icon a-icon-star-medium a-star-medium-4-5 averageStarRating'}).find(
                "span")
            product["Rating"] = rating.text.split()[0]
            logger.debug("Product Rating: {rate}".format(rate=product["Rating"]))
        except Exception as e:
            logger.exception(e.message)

        today_date = datetime.date.today()
        product["TodayDate"] = today_date.strftime("%B %d, %Y")

        exists = self.utils.exists_product_in_db(product["ASIN"])
        if exists:
            print "update database in inserting products"
            self.utils.update_product_into_db(product, category_name)
        else:
            self.utils.insert_product_into_db(product, category_name)
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
                most_recent = '&sortBy=recent'
                if next_url is not None:
                    next_url = next_url + most_recent
                else:
                    break
                next_page = common.request_page(next_url)
                review_links = next_page.find_all('a', {
                    'class': 'a-size-base a-link-normal review-title a-color-base a-text-bold'})
                for link in review_links:
                    review_url = '{base_url}{url}'.format(base_url=self.base_url, url=link.get('href').encode('utf-8'))
                    logger.debug('review url: {url}'.format(url=review_url))
                    if not self.utils.exists_review_in_db(review_url):
                        logger.debug('review {link} does not exists in the database'.format(link=review_url))
                        self.scrap_review(review_url, product_dict["ASIN"])

                    else:
                        logger.debug('review {link} already exists in the database'.format(link=review_url))
                        continue

                next_link = next_page.find('li', {'class': 'a-last'})
                next_url = '{base_url}{url}'.format(base_url=self.base_url,
                                                    url=next_link.find('a').get('href').encode('utf-8'))
                total_reviews = self.utils.get_total_num_reviews(product_dict["ASIN"]).replace(',', '')
                scraped_reviews = self.utils.get_scraped_reviews(product_dict["ASIN"])
                global percent_scraped_reviews
                global status
                print product_dict["ASIN"]
                print total_reviews
                print scraped_reviews
                if total_reviews is not None and scraped_reviews is not None:
                    if not total_reviews == 0:
                        percent_scraped_reviews = (float(scraped_reviews) / float(total_reviews)) * 100
                        print percent_scraped_reviews
                if 0 <= int(total_reviews) <= 100:
                    logger.debug('checking if scraped reviews are more then 90%')
                    if percent_scraped_reviews >= 90:
                        logger.debug('scraped reviews >= 90% True')
                        status = 1
                        self.utils.update_status(product_dict["ASIN"], status)
                        break
                    else:
                        logger.debug('scraped reviews >= 90% False')
                        status = 0
                        self.utils.update_status(product_dict["ASIN"], status)
                        continue
                elif 101 <= int(total_reviews) <= 1000:
                    logger.debug('checking if scraped reviews are more then 50%')
                    if percent_scraped_reviews >= 50:
                        logger.debug('scraped reviews >= 50% True')
                        status = 1
                        self.utils.update_status(product_dict["ASIN"], status)
                        break
                    else:
                        logger.debug('scraped reviews >= 50% False')
                        status = 0
                        self.utils.update_status(product_dict["ASIN"], status)
                        continue
                elif 1001 <= int(total_reviews) <= 5000:
                    logger.debug('checking if scraped reviews are more then 25%')
                    if percent_scraped_reviews >= 25:
                        logger.debug('scraped reviews >= 25% True')
                        status = 1
                        self.utils.update_status(product_dict["ASIN"], status)
                        break
                    else:
                        logger.debug('scraped reviews >= 25% False')
                        status = 0
                        self.utils.update_status(product_dict["ASIN"], status)
                        continue
                elif 5001 <= int(total_reviews) <= 10000:
                    logger.debug('checking if scraped reviews are more then 10%')
                    if percent_scraped_reviews >= 1:
                        logger.debug('scraped reviews >= 10% True')
                        status = 1
                        self.utils.update_status(product_dict["ASIN"], status)
                        break
                    else:
                        logger.debug('scraped reviews >= 10% False')
                        status = 0
                        self.utils.update_status(product_dict["ASIN"], status)
                        continue
                else:
                    logger.debug('checking if scraped reviews are more then 1%')
                    if percent_scraped_reviews >= 0.5:
                        logger.debug('scraped reviews >= 1% True')
                        status = 1
                        self.utils.update_status(product_dict["ASIN"], status)
                        break
                    else:
                        logger.debug('scraped reviews >= 1% False')
                        status = 0
                        self.utils.update_status(product_dict["ASIN"], status)
                        continue

            except AttributeError as e:
                logger.exception('{exception}'.format(exception=e.message))
                break  # breaking from loop when next link not found

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
        self.utils.insert_review_into_db(review_dict, product_asin)
        self.utils.insert_reviewer_into_db(review_dict)
