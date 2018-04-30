URLS = {
    "BaseUrl": "https://www.amazon.com",
    "NewReleases": "/gp/new-releases/",
    "SportsOutdoors": "/gp/new-releases/sporting-goods/",
    "FanShop": "3386071/",
    "AutoAccess": "374773011/"
}

QUERIES = {
    "InsertProduct": "INSERT INTO crawper.products(product_asin, product_title, product_price, reviews_link,"
                     "category_name, product_link, total_reviews, product_rank, image_link, product_rating, last_scraped_date) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ",

    "InsertReview": "INSERT INTO crawper.reviews(review_link, product_asin, review_title, review_text, reviewer_id, "
                    "review_date, review_rate) VALUES (%s, %s, %s, %s, %s, %s, %s);",

    "ProductExists": "SELECT EXISTS(SELECT product_asin FROM crawper.products WHERE product_asin=%s);",

    "InsertReviewer": "INSERT INTO crawper.reviewers(reviewer_id, reviewer_name, profile_link, total_reviews, "
                      "creduality_score) VALUES (%s, %s, %s, %s, %s); ",

    "ReviewerExists": "SELECT EXISTS(SELECT reviewer_id FROM crawper.reviewers WHERE reviewer_id=%s);",

    "ExistsReview": "SELECT EXISTS (SELECT review_link FROM crawper.reviews WHERE review_link=%s);",

    "UpdateProduct": "UPDATE crawper.products SET product_title=%s, product_price=%s, reviews_link=%s, "
                     "category_name=%s, product_link=%s, total_reviews=%s, product_rank=%s, image_link=%s, "
                     "product_rating=%s, last_scraped_date=%s WHERE product_asin=%s;",

    "GetTotalReviewCount": "SELECT total_reviews FROM crawper.products WHERE product_asin=%s;",

    "GetScrapedProductCount": "SELECT COUNT(*) FROM crawper.reviews WHERE product_asin=%s;",

    "UpdateStatus": "UPDATE crawper.products SET status=%s WHERE product_asin=%s;"

}
