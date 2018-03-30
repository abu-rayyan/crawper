QUERIES = {
    "GetCategories": "SELECT category_name FROM crawper.categories;",

    "ExistsCategory": "SELECT EXISTS(SELECT category_name FROM crawper.categories WHERE category_name=%s);",

    "GetCategoryProducts": "SELECT product_title, product_price, product_link, total_reviews, product_rank, "
                           "image_link, product_asin FROM crawper.products WHERE category_name=%s; ",
    "GetProduct": "SELECT product_asin, product_title, product_price, product_link, total_reviews, product_rank, "
                  "image_link, product_rating FROM crawper.products WHERE product_asin=%s AND category_name=%s; ",
    "SearchProduct": "SELECT product_asin, product_title, product_price, total_reviews, image_link, product_link, "
                     "category_name FROM crawper.products Where product_title ILIKE %s;",
    "GetSentimentLabels": "SELECT reviews_analysis.sentiment_label FROM crawper.reviews, crawper.reviews_analysis "
                          "WHERE crawper.reviews.review_link = crawper.reviews_analysis.review_link AND "
                          "crawper.reviews.product_asin=%s; ",
    "GetWordCategory": "SELECT reviews_analysis.word_count_category FROM crawper.reviews, crawper.reviews_analysis "
                       "WHERE crawper.reviews.review_link = crawper.reviews_analysis.review_link AND "
                       "crawper.reviews.product_asin=%s; ",

    "Sum_of_total_num_of_reviews": "SELECT total_reviews from crawper.products;",

    "GetCredulityScoreOfProduct": "SELECT reviews_analysis.credulity_score FROM crawper.reviews, crawper.reviews_analysis "
                       "WHERE crawper.reviews.review_link = crawper.reviews_analysis.review_link AND "
                       "crawper.reviews.product_asin=%s;",

    "GetParticipationHistory": "SELECT reviewers.participation_history FROM crawper.reviewers, crawper.reviews "
                       "WHERE crawper.reviews.reviewer_id = crawper.reviewers.reviewer_id AND "
                       "crawper.reviews.product_asin=%s;",

    "GetCommonPhrase": "SELECT reviews_analysis.common_phrase, reviews.review_rate FROM crawper.reviews_analysis, crawper.reviews "
                       "WHERE crawper.reviews.review_link = crawper.reviews_analysis.review_link AND "
                       "crawper.reviews.product_asin=%s;",

    "MissingMiddle": "SELECT reviews.review_rate FROM crawper.reviews WHERE crawper.reviews.product_asin=%s;",

    "GetMSDR": "SELECT msdr from crawper.products where product_asin=%s;"
}