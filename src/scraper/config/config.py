URLS = {
    "BaseUrl": "https://www.amazon.com",
    "NewReleases": "/gp/new-releases/",
    "SportsOutdoors": "/gp/new-releases/sporting-goods/",
    "FanShop": "3386071/",
    "AutoAccess": "374773011/"
}

QUERIES = {
    "InsertProduct": "INSERT INTO crawper.products(product_asin, product_title, product_price, reviews_link,"
                     "category_name, product_link, total_reviews) VALUES (%s, %s, %s, %s, %s, %s, %s); ",
    "InsertReview": "INSERT INTO crawper.reviews("
                    "review_link, product_asin, review_title, review_text, review_rate, reviewer_id, review_date)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s); "
}
