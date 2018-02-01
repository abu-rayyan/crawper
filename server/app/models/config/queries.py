QUERIES = {
    "GetCategories": "SELECT category_name FROM crawper.categories;",

    "ExistsCategory": "SELECT EXISTS(SELECT category_name FROM crawper.categories WHERE category_name=%s);",

    "GetCategoryProducts": "SELECT product_title, product_price, product_link, total_reviews, product_rank, "
                           "image_link, product_asin FROM crawper.products WHERE category_name=%s; ",
    "GetProduct": "SELECT product_asin, product_title, product_price, product_link, total_reviews, product_rank, "
                  "image_link FROM crawper.products WHERE product_asin=%s AND category_name=%s; ",
    "SearchProduct": "SELECT product_title FROM crawper.products Where product_title LIKE %s;"
}
