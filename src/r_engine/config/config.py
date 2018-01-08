QUERIES = {
    "GetProduct": "SELECT product_asin, product_title, product_price, reviews_link, category_name, product_link, "
                  "total_reviews FROM crawper.products WHERE product_asin=%s; ",

    "GetProductReviews": "SELECT review_link, product_asin, review_title, review_text, review_rate, reviewer_id, "
                         "review_date FROM crawper.reviews WHERE product_asin=%s; ",

    "GetProductsAsin": "SELECT product_asin FROM crawper.products;",

    "InsertReviewStat": "INSERT INTO crawper.reviews_analysis(review_link, review_length, word_count_category, "
                        "sentiment_score, sentiment_label, common_phrase, credulity_score, review_scores) VALUES (%s, "
                        "%s, %s, %s, %s, %s, %s, %s); ",

    "GetReviewerIds": "SELECT reviewer_id FROM crawper.reviewers;",

    "GetTotalReviewsOfReviewer": "SELECT review_rate FROM crawper.reviews where reviewer_id = %s;",

    "UpdateReviewerCredualityScore": "UPDATE crawper.reviewers SET total_reviews=%s, creduality_score=%s, "
                                     "participation_history=%s WHERE reviewer_id=%s;",

    "GetProductReviewsText": "SELECT review_text FROM crawper.reviews where product_asin=%s;",

    "GetReviewerCreaduality": "SELECT creduality_score FROM crawper.reviewers where reviewer_id = %s;",

    "GetProductReviewers": "SELECT review_rate, reviewer_id FROM crawper.reviews where product_asin=%s;",

    "Get45StarProductReviews": "SELECT review_text FROM crawper.reviews where product_asin=%s AND review_rate >= '4.0';",

    "GetReviewersWithOneReview": "SELECT reviewer_id FROM crawper.reviewers where total_reviews=1;",

    "Get45StarReviewers": "SELECT reviewer_id FROM crawper.reviews where review_rate >= 4;",

    "GetReviewerReviewsDate": "SELECT review_date FROM crawper.reviews where reviewer_id=%s AND review_rate >= 4;",

    "GetTotalNoReviewesOfReviewer": "SELECT total_reviews FROM crawper.reviewers where reviewer_id=%s;",

    "GetReviewer45StarReviews": "SELECT review_text FROM crawper.reviews where reviewer_id = %s and review_rate >= 4;",

    "GetRatesOfReviewsOfProduct": "SELECT review_rate FROM crawper.reviews where product_asin=%s;",

    "GetNoOf3StarReviewsOfProduct": "SELECT count(*) FROM crawper.reviews where product_asin = %s and review_rate=3;",

    "GetNoOf1to2StarReviewsOfProduct": "SELECT count(*) FROM crawper.reviews where product_asin = %s and review_rate "
                                       "<= 2; "
}
