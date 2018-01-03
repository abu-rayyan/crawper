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
    "UpdateReviewerCredualityScore": "UPDATE crawper.reviewers SET total_reviews=%s, creduality_score=%s WHERE reviewer_id=%s;",
    "GetProductReviewsText": "SELECT review_text FROM crawper.reviews where product_asin=%s;",
    "GetReviewerCreaduality": "SELECT creduality_score FROM crawper.reviewers where reviewer_id = %s;"
}
