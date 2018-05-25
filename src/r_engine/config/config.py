QUERIES = {
    "GetProduct": "SELECT product_asin, product_title, product_price, reviews_link, category_name, product_link, "
                  "total_reviews FROM crawper.products WHERE product_asin=%s; ",

    "GetProductReviews": "SELECT review_link, product_asin, review_title, review_text, review_rate, reviewer_id, "
                         "review_date FROM crawper.reviews WHERE product_asin=%s; ",

    "GetProductsAsin": "SELECT product_asin FROM crawper.products;",
    "GetAsinsWithZeroRank": "SELECT product_asin FROM crawper.products WHERE product_rank = '0';",

    "InsertReviewStat": "INSERT INTO crawper.reviews_analysis(review_link, review_length, word_count_category, "
                        "sentiment_score, sentiment_label, common_phrase, credulity_score, review_scores, word_volume_comp_trigger) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); ",

    "GetReviewerIds": "SELECT reviewer_id FROM crawper.reviews WHERE product_asin=%s AND status is null;",

    "GetTotalReviewsOfReviewer": "SELECT review_rate FROM crawper.reviews where reviewer_id = %s ;",

    "UpdateReviewerCredualityScore": "UPDATE crawper.reviewers SET total_reviews=%s, creduality_score=%s, "
                                     "participation_history=%s, one_off_trigger=%s, "
                                      "multiple_single_day_trigger=%s WHERE reviewer_id=%s;",

    "GetProductReviewsText": "SELECT review_text FROM crawper.reviews where product_asin=%s;",

    "GetReviewerCreaduality": "SELECT creduality_score, one_off_trigger, multiple_single_day_trigger, total_reviews "
                              "FROM crawper.reviewers where reviewer_id = %s;",

    "Get45StarProductReviews": "SELECT review_text FROM crawper.reviews where product_asin=%s AND review_rate >= '4.0';",

    "GetReviewersWithOneReview": "SELECT reviewer_id FROM crawper.reviewers where total_reviews=1;",

    "Get45StarReviewers": "SELECT reviewer_id FROM crawper.reviews where review_rate >= 4;",

    "GetReviewerReviewsDate": "SELECT review_date FROM crawper.reviews where reviewer_id=%s AND review_rate >= 4;",

    "GetTotalNoReviewesOfReviewer": "SELECT total_reviews FROM crawper.reviewers where reviewer_id=%s;",

    "GetReviewer45StarReviews": "SELECT review_text FROM crawper.reviews where reviewer_id = %s and review_rate >= 4;",

    "git GetRatesOfReviewsOfProduct": "SELECT review_rate FROM crawper.reviews where product_asin=%s;",

    "GetNoOf3StarReviewsOfProduct": "SELECT count(*) FROM crawper.reviews where product_asin = %s and review_rate=3;",

    "GetNoOf1to2StarReviewsOfProduct": "SELECT count(*) FROM crawper.reviews where product_asin = %s and review_rate "
                                       "<= 2; ",
    "GetReviewerIdsOfProductReviews": "SELECT reviewer_id FROM crawper.reviews where product_asin=%s;",

    "GetReviewerParticipationHistory": "SELECT participation_history FROM crawper.reviewers where reviewer_id = %s;",

    "GetProductReviewsDates": "SELECT review_date FROM crawper.reviews where product_asin=%s;",

    "GetNoOfTodayReviewsOfProduct": "SELECT count(*) FROM crawper.reviews where product_asin=%s and review_date=%s;",

    "GetReviewsIdsOfReviewer": "SELECT review_link FROM crawper.reviews where reviewer_id=%s;",

    "GetReviewScore": "SELECT review_scores FROM crawper.reviews_analysis where review_link=%s;",

    "UpdateReviewScore": "UPDATE crawper.reviews_analysis SET review_scores=%s WHERE review_link=%s;",

    "GetProductRank": "SELECT product_rank FROM crawper.products where product_asin=%s;",

    "UpdateProductRank": "UPDATE crawper.products SET product_rank=%s WHERE product_asin=%s;",

    "GetReviewText": "SELECT review_text FROM crawper.reviews WHERE review_link=%s;",

    "GetDistinctCategories": "SELECT category_name FROM crawper.products WHERE product_asin=%s;",

    "CheckCategories": "SELECT no_of_products FROM crawper.word_volume_comparison WHERE category_name=%s;",

    "GetProductasinFromProducts": "SELECT product_asin FROM crawper.products WHERE category_name=%s;",

    "GetReviewsUsingProductasin": "SELECT review_text FROM crawper.reviews WHERE product_asin=%s;",

    "InsertAvgWordLen": "INSERT INTO crawper.word_volume_comparison(category_name, avg_word_len, no_of_products)\
    VALUES (%s,%s, %s);",

    "UpdateAvgLength": "UPDATE crawper.word_volume_comparison SET avg_word_len=%s, no_of_products=%s WHERE category_name=%s",

    "GetReviewsProductasin": "SELECT reviews_analysis.review_length, reviews_analysis.review_link "
                       "FROM crawper.reviews, crawper.reviews_analysis "
                       "WHERE crawper.reviews.product_asin=%s AND crawper.reviews.review_link=crawper.reviews_analysis.review_link;",

    "GetCategoryUsingProductasin": "SELECT category_name FROM crawper.products WHERE product_asin=%s;",

    "GetAvgWordLengthUsingCategory": "SELECT avg_word_len FROM crawper.word_volume_comparison WHERE category_name=%s;",

    "InsertTriggerInReviewAnalysis": "UPDATE crawper.reviews_analysis SET word_volume_comp_trigger=%s "
                "WHERE crawper.reviews_analysis.review_link=%s;",

    "GetDistinctProductAsin": "SELECT DISTINCT(product_asin) from crawper.reviews;",

    "GetMinMaxDate": "SELECT  crawper.products.total_reviews, COUNT(reviews.review_text), "
                              "MAX(to_date(nullif(reviews.review_date,''), 'Month DD, YYYY')), "
                              "MIN(to_date(nullif(reviews.review_date,''), 'Month DD, YYYY')) "
                              "FROM crawper.products, crawper.reviews "
                              "WHERE crawper.reviews.product_asin=%s AND crawper.products.product_asin=%s "
	                          "Group By crawper.products.total_reviews;",

    "GetReviewRate": "SELECT review_rate FROM crawper.reviews where product_asin=%s;",

    "InsertAbnormalReview": "INSERT INTO crawper.abnormal_review_analysis(product_asin, total_reviews, total_review_scraped, "
                        "min_date, max_date, no_of_1star, no_of_2star, no_of_3star, no_of_4star, no_of_5star, abnormal_trigger) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ",

    "GetProductAsin": "SELECT product_asin from crawper.products;",

    "UpdateStatus": "UPDATE crawper.products SET status=%s WHERE product_asin=%s;",

    "GetTotalReviews": "SELECT total_reviews FROM crawper.products WHERE product_asin=%s;",

    "GetTotalScraped": "SELECT COUNT(*) FROM crawper.reviews WHERE product_asin=%s;",

    "ExistsReviewLink": "SELECT EXISTS(SELECT review_link FROM crawper.reviews_analysis WHERE review_link=%s);",

    "GetData": "SELECT reviewer_id, total_reviews FROM crawper.reviewers;",

    "UpdateOneOffTrigger": "UPDATE crawper.reviewers SET one_off_trigger=%s WHERE reviewer_id=%s;",

    "UpdateStatusReviews": "UPDATE crawper.reviews SET status=%s WHERE product_asin=%s;",

    "GetUrls": "select categories.category_link from crawper.word_volume_comparison, crawper.categories "
                "where crawper.word_volume_comparison.no_of_products < 30 "
                "AND crawper.word_volume_comparison.category_name=crawper.categories.category_name "
                "AND crawper.categories.category_link is NOT null;",

    "ExistsProductAbnormal": "SELECT EXISTS(SELECT product_asin FROM crawper.abnormal_review_analysis WHERE product_asin=%s);",

    "UpdateAbnormalTrigger": "UPDATE crawper.abnormal_review_analysis SET total_reviews=%s, total_review_scraped=%s, "
                        "min_date=%s, max_date=%s, no_of_1star=%s, no_of_2star=%s, no_of_3star=%s, no_of_4star=%s, "
                        "no_of_5star=%s, abnormal_trigger=%s WHERE product_asin=%s;"

}
