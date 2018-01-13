URLS = {
    "BaseUrl": "https://www.amazon.com",
    "NewReleases": "/gp/new-releases/",
    "SportsOutdoors": "/gp/new-releases/sporting-goods/",
    "FanShop": "3386071/",
    "AutoAccess": "374773011/"
}

QUERIES = {
    "InsertProduct": "INSERT INTO crawper.products(product_asin, product_title, product_price, reviews_link,"
                     "category_name, product_link, total_reviews, product_rank, image_link) VALUES (%s, %s, %s, %s, "
                     "%s, %s, %s, %s, %s); ",

    "InsertReview": "INSERT INTO crawper.reviews(review_link, product_asin, review_title, review_text, reviewer_id, "
                    "review_date, review_rate) VALUES (%s, %s, %s, %s, %s, %s, %s);",

    "ProductExists": "SELECT EXISTS(SELECT product_asin FROM crawper.products WHERE product_asin=%s);",

    "InsertReviewer": "INSERT INTO crawper.reviewers(reviewer_id, reviewer_name, profile_link, total_reviews, "
                      "creduality_score) VALUES (%s, %s, %s, %s, %s); "
}
