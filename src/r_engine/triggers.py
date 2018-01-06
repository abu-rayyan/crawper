import logging
import math

from textblob import TextBlob
from utility import UtilityFunctions

logger = logging.getLogger(__name__)


class Triggers:
    def __init__(self):
        logger.debug('initializing triggers generator')
        self.utility_methods = UtilityFunctions()

    def get_overlapping_trigger(self, product_asin):
        """
        Checks and returns trigger if over-lapping reviews exists
        :param product_asin: asin no of product
        :return: bool
        """
        logger.debug('generating overlapping reviews trigger')
        product_reviewers = self.utility_methods.get_reviewers_from_db(product_asin)

        for item in product_reviewers:
            if not float(item[0]) >= 4:
                product_reviewers.remove(item)

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

    def get_words_vol_comparison_trigger(self, product_asin):
        """
        Checks and generates Words-Volume-Comparison trigger
        :param product_asin: asin no of product
        :return: bool
        """
        logger.debug('generating words volume comparison trigger')
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

    def get_one_off_trigger(self):
        """
        Checks and generates One-Off-Review trigger
        :return: bool
        """
        logger.debug('generating one off reviewer trigger ')
        reviewer_ids = self.utility_methods.get_reviewers_with_one_review_from_db()
        all_reviewer_ids = self.utility_methods.get_all_reviewers_with_four_five_stars()

        return any(reviewer_id in all_reviewer_ids for reviewer_id in reviewer_ids)

    def get_multiple_single_day_reviews_trigger(self, reviewer_id):
        """
        Checks and generates Multiple-Single-Day-Review trigger
        :param reviewer_id: Id of the reviewer
        :return: bool
        """
        logger.debug(
            'generating multiple single day reviews trigger for reviewer {reviewer}'.format(reviewer=reviewer_id))
        reviews_dates = self.utility_methods.get_reviewer_reviewes_date_from_db(reviewer_id)
        dates_list = []

        for review_date in reviews_dates:
            dates_list.append(review_date[0])

        if self.utility_methods.get_no_duplicates(dates_list) > 3:
            return True
        else:
            return False

    def get_duplicated_reviews_trigger(self, reviewer_id):
        """
        Checks and generates Duplicated-Reviews trigger
        :param reviewer_id: Id of reviewer
        :return: bool
        """
        logger.debug('generating duplicated reviews trigger for reviewer {id}'.format(id=reviewer_id))
        total_reviews = self.utility_methods.get_total_no_of_reviewes_of_reviewer_from_db(reviewer_id)[0][0]
        reviews = self.utility_methods.get_four_five_star_reviews_of_reviewer_from_db(reviewer_id)

        reviews_list = []
        for review in reviews:
            reviews_list.append(review[0])
        review_set = set(reviews_list)

        if len(reviews_list) > 0.05 * total_reviews and len(review_set) == 1:
            return True
        else:
            return False

    def get_rating_trend_trigger(self, product_asin):
        """
        Checks and generates Rating-Trend trigger
        :param product_asin: asin no of product
        :return: bool
        """
        logger.debug('generating rating trend trigger for product {asin}'.format(asin=product_asin))
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
        no_last_reviews = no_first_reviews + (int(math.ceil(no_first_reviews*0.8)))

        for item in rate_list[no_first_reviews:no_last_reviews+1]:
            no_last_reviews_list.append(item)

        check_last_bool = all(item >= 4 for item in no_last_reviews_list)

        if check_first_bool and check_last_bool:
            return True
        else:
            return False


    def get_three_star_ratio_check_trigger(self, product_asin):
        logger.debug('generating 3 start ratio check trigger for product {asin}'.format(asin=product_asin))

    def get_total_triggers(self, product_asin):
        logger.debug('getting total number of triggers for product {asin}'.format(asin=product_asin))

    def get_abnormal_review_trigger(self):
        logger.debug('generating abormal review category participation trigger')

    def get_repeated_remarks_trigger(self, product_asin):
        logger.debug('generating repeated remarks trigger for product {asin}'.format(asin=product_asin))

    def get_review_spikes_trigger(self, product_asin):
        logger.debug('generating review spikes trigger for product {asin}'.format(asin=product_asin))
