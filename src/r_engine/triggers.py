import logging
import math
import nltk
import datetime

from textblob import TextBlob
from dateutil import parser
from datetime import timedelta
from utility import UtilityFunctions

# noinspection SpellCheckingInspection
nltk.download('punkt')
logger = logging.getLogger(__name__)


# noinspection SpellCheckingInspection
class Triggers:
    def __init__(self, conn, cursor, pool):
        logger.debug('initializing triggers generator')
        self.utility_methods = UtilityFunctions(conn, cursor, pool)

    # Trigger is activated if the same reviewers of a product were also the reviewers of 10 or more other products that they also gave 4-5 stars
    def get_overlapping_trigger(self, product_asin):

        """
        Checks and returns trigger if over-lapping reviews exists
        :param product_asin: asin no of product
        :return: bool
        """
        logger.debug('generating overlapping reviews trigger')
        try:
            product_reviewers = self.utility_methods.get_reviewers_from_db(product_asin)
            # fetch all reviiews from database and check if their length is greater than 4 otherwise remove them
            print product_reviewers
            for item in product_reviewers:
                if not float(item[0]) >= 4:
                    product_reviewers.remove(item)
            # fetch all reviiews from database
            all_product_reviewers = self.utility_methods.get_all_reviewers_from_db(product_asin)
            count = 0  # TODO: Consider 4 to 5 star reviews only, need change in DB as well
            for reviewer in product_reviewers:
                for reviewers in all_product_reviewers:
                    if reviewer in reviewers:
                        count += 1

            if count >= 10:
                return True
            else:
                return False
        except Exception as e:
            logger.exception(e.message)
            return None
    '''
    # Trigger is activated if the length of a 4-5 star review is less than 25% or more than double the length of the average review of the product
    def get_words_vol_comparison_trigger(self, product_asin):
        """
        Checks and generates Words-Volume-Comparison trigger
        :param product_asin: asin no of product
        :return: bool
        """
        logger.debug('generating words volume comparison trigger')
        try:
            reviews_length = []
            avg_review_length = 0
            reviews_text = self.utility_methods.get_product_reviews_with_four_five_stars(product_asin)
            if reviews_text:
                for review_text in reviews_text:
                    blob = TextBlob(review_text[0].decode('utf-8'))
                    reviews_length.append(len(blob.words))
                avg_review_length = sum(reviews_length) / len(reviews_length)

            trigger = False
            for review_text in reviews_text:
                blob = TextBlob(review_text[0].decode('utf-8'))
                if len(blob.words) < 0.25 * avg_review_length or len(blob.words) > 2 * avg_review_length:
                    trigger = True

            return trigger
        except Exception as e:
            logger.exception(e.message)
            return None
    '''

    # Trigger is activated for reviewers giving only 1 review that is also a 4-5 star review
    def get_one_off_trigger(self):
        """
        Checks and generates One-Off-Review trigger
        :return: bool
        """
        logger.debug('generating one off reviewer trigger ')
        try:
            reviewer_ids = self.utility_methods.get_reviewers_with_one_review_from_db()
            all_reviewer_ids = self.utility_methods.get_all_reviewers_with_four_five_stars()

            return any(reviewer_id in all_reviewer_ids for reviewer_id in reviewer_ids)
        except Exception as e:
            logger.exception(e.message)
            return None

    # Trigger is activated if there are more than 3 same-day 4-5 star reviews from the same reviewer
    def get_multiple_single_day_reviews_trigger(self, reviewer_id):
        """
        Checks and generates Multiple-Single-Day-Review trigger
        :param reviewer_id: Id of the reviewer
        :return: bool
        """
        logger.debug(
            'generating multiple single day reviews trigger for reviewer {reviewer}'.format(reviewer=reviewer_id))
        try:
            reviews_dates = self.utility_methods.get_reviewer_reviewes_date_from_db(reviewer_id)
            dates_list = []

            for review_date in reviews_dates:
                dates_list.append(review_date[0])

            if self.utility_methods.get_no_duplicates(dates_list) > 3:
                return True
            else:
                return False
        except Exception as e:
            logger.exception(e.message)
            return None

        # Trigger is activated if more than 5% of a reviewers total reviews are 4-5 stars and
        # are also word-for-word duplicates

    def get_duplicated_reviews_trigger(self, reviewer_id, total_reviews):
        """
        Checks and generates Duplicated-Reviews trigger
        :param reviewer_id: Id of reviewer
        :return: bool
        """
        try:
            logger.debug('generating duplicated reviews trigger for reviewer {id}'.format(id=reviewer_id))
            reviews = self.utility_methods.get_four_five_star_reviews_of_reviewer_from_db(reviewer_id)

            reviews_list = []
            for review in reviews:
                reviews_list.append(review[0])
            review_set = set(reviews_list)

            if len(reviews_list) > 0.05 * total_reviews and len(review_set) == 1:
                return True
            else:
                return False
        except Exception as e:
            logger.exception(e.message)
            return False

        # Trigger is activated if the first 5% of the ratings a product received were (1-2 stars) were followed by a  \
        # sudden increase of (4-5 stars) ratings of more than 80% of the total number of initial (1-2 star) ratings
        # the product received
    def get_rating_trend_trigger(self, product_asin):
        """
        Checks and generates Rating-Trend trigger
        :param product_asin: asin no of product
        :return: bool
        """
        logger.debug('generating rating trend trigger for product {asin}'.format(asin=product_asin))
        try:
            review_rates = self.utility_methods.get_review_rate_of_reviews_of_product(product_asin)
            rate_list = []
            no_first_reviews_list = []
            no_last_reviews_list = []

            for rate in review_rates:
                rate_list.append(rate[0])

            no_first_reviews = int(math.ceil(len(rate_list) * 0.05))

            for item in range(no_first_reviews):
                no_first_reviews_list.append(rate_list[item])

            check_first_bool = all(item <= 2 for item in no_first_reviews_list)
            no_last_reviews = no_first_reviews + (int(math.ceil(no_first_reviews * 0.8)))

            for item in rate_list[no_first_reviews:no_last_reviews + 1]:
                no_last_reviews_list.append(item)

            check_last_bool = all(item >= 4 for item in no_last_reviews_list)

            if check_first_bool and check_last_bool:
                return True
            else:
                return False
        except Exception as e:
            logger.exception(e.message)
            return None

        # Trigger is activated if trigger # 9 is activated and the percentage of 3 star ratings for a
        # product is less than 20% of the total 1-2 star ratings
    def get_three_star_ratio_check_trigger(self, product_asin):
        """
        Get three star reviews check trigger based on rating trend trigger
        :param product_asin: asin no of product
        :return: bool
        """
        logger.debug('generating 3 start ratio check trigger for product {asin}'.format(asin=product_asin))
        try:
            if self.get_rating_trend_trigger(product_asin):
                three_star_reviews = \
                    self.utility_methods.get_total_no_three_star_reviews_of_product_from_db(product_asin)[0][0]
                one_two_star_reviews = \
                    self.utility_methods.get_total_no_one_two_star_reviews_of_product_from_db(product_asin)[0][0]
                three_star_percent = (float(three_star_reviews) / float(
                    one_two_star_reviews)) * 100 if one_two_star_reviews else 0
                if three_star_percent < 20.0:
                    return True
                else:
                    return False
            else:
                logger.debug('rating trend trigger is not activated')
                return False
        except Exception as e:
            logger.exception(e.message)
            return None

        # Trigger is activated if the concentration of 4-5 star ratings is more than what would expect to see from a
        # reviewer for any category based on their participation history from column R

    def get_abnormal_review_trigger(self, product_asin):
        ProductAnalysis = {
            "ProductAsin": None,
            "TotatReviews": None,
            "TotalReviewsScraped": None,
            "MaxDate": None,
            "MinDate": None,
            "NoOf5star": None,
            "NoOf4star": None,
            "NoOf3star": None,
            "NoOf2star": None,
            "NoOf1star": None,
            "trigger": None
        }

        rating = self.utility_methods.get_all_rating_stars(product_asin)
        r_5 = 0
        r_4 = 0
        r_3 = 0
        r_2 = 0
        r_1 = 0
        try:
            for rate in rating:
                if math.floor(rate[0]) == 5.0:
                    r_5 += 1
                elif math.floor(rate[0]) == 4.0:
                    r_4 += 1
                elif math.floor(rate[0]) == 3.0:
                    r_3 += 1
                elif math.floor(rate[0]) == 2.0:
                    r_2 += 1
                elif math.floor(rate[0]) == 1.0:
                    r_1 += 1
                else:
                    continue
        except Exception as e:
            print(e.message)
        counttext_max_min_date = self.utility_methods.get_min_max_date(product_asin)

        ProductAnalysis["ProductAsin"] = product_asin
        ProductAnalysis["TotatReviews"] = (counttext_max_min_date[0][0])
        ProductAnalysis["TotalReviewsScraped"] = (counttext_max_min_date[0][1])
        ProductAnalysis["MaxDate"] = (counttext_max_min_date[0][2])
        ProductAnalysis["MinDate"] = (counttext_max_min_date[0][3])
        ProductAnalysis["NoOf1star"] = r_1
        ProductAnalysis["NoOf2star"] = r_2
        ProductAnalysis["NoOf3star"] = r_3
        ProductAnalysis["NoOf4star"] = r_4
        ProductAnalysis["NoOf5star"] = r_5
        if ProductAnalysis["NoOf3star"] or ProductAnalysis["NoOf2star"] or ProductAnalysis["NoOf1star"]:
            trigger = '0'
        else:
            trigger = '1'
        ProductAnalysis["trigger"] = trigger
        if not self.utility_methods.check_product_in_abnormal(product_asin):
            self.utility_methods.insert_in_abnormal_review_table(ProductAnalysis)
        else:
            self.utility_methods.update_abnormal_trigger(ProductAnalysis)
        print(ProductAnalysis)
        return trigger

    '''
    def get_abnormal_review_trigger(self, product_asin):
        """
        Calculates abnormal reviews trigger
        :param product_asin: product asin
        :return: bool
        """
        logger.debug('generating abormal review category participation trigger for product {asin}'.format(
            asin=product_asin.decode('utf-8')))
        try:
            reviewer_ids = self.utility_methods.get_reviews_reviewer_ids_from_db(product_asin)
            labels_list = []

            if reviewer_ids:
                for reviewer_id in reviewer_ids:
                    participation_label = self.utility_methods.get_reviewers_participation_from_db(reviewer_id[0])
                    if participation_label:
                        labels_list.append(participation_label[0][0])

            labels_set = set(labels_list)
            if len(labels_set) == 1:
                return True
            else:
                return False
        except Exception as e:
            logger.exception(e.message)
            return None
    '''

    def get_review_spikes_trigger(self, product_asin):
        """
        Calculates review spikes trigger
        :param product_asin: product asin
        :return: bool
        """
        logger.debug('generating review spikes trigger for product {asin}'.format(asin=product_asin.decode('utf-8')))
        try:
            dates_list = self.utility_methods.get_product_reviews_dates_from_db(product_asin)
            date_list = []

            if dates_list:
                for date in dates_list:
                    dt = parser.parse(date[0])
                    date_list.append(dt)

                oldest_date = min(date_list)
                todays_date = datetime.datetime.today()
                yesterday_date = todays_date - timedelta(days=1)
                total_days = yesterday_date - oldest_date
                date_to_remove = todays_date.strftime('%Y-%m-%d')

                present_day_reviews_count = 0
                for date in date_list:
                    if date == parser.parse(date_to_remove):
                        present_day_reviews_count += 1
                        date_list.remove(date)

                avg_reviews_per_day = float(len(date_list)) / float(total_days.days)
                avg_reviews_per_day = math.ceil(avg_reviews_per_day)

                if present_day_reviews_count <= avg_reviews_per_day:
                    return False
                else:
                    return True
        except Exception as e:
            logger.exception(e.message)
            return None
