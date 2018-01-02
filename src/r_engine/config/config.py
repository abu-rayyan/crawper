QUERIES = {
    "GetProduct": "SELECT product_asin, product_title, product_price, reviews_link, category_name, product_link, "
                  "total_reviews FROM crawper.products WHERE product_asin=%s; ",
    "GetProductReviews": "SELECT review_link, product_asin, review_title, review_text, review_rate, reviewer_id, "
                         "review_date FROM crawper.reviews WHERE product_asin=%s; ",
    "GetProductsAsin": "SELECT product_asin FROM crawper.products;",
    "InsertReviewStat": "INSERT INTO crawper.reviews_analysis(review_link, review_length, word_count_category, "
                        "sentiment_score, sentiment_label, common_phrase, credulity_score, review_scores) VALUES (%s, "
                        "%s, %s, %s, %s, %s, %s, %s); "
}
