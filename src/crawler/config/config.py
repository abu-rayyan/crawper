URLS = {
    "BaseUrl": "https://www.amazon.com",
    "NewReleases": "/gp/new-releases/",
    "SportsOutdoors": "/gp/new-releases/sporting-goods/",
    "FanShop": "3386071/",
    "AutoAccess": "374773011/"
}

QUERIES = {
    "InsertCategory": "INSERT INTO crawper.categories(category_name) VALUES (%s);",
    "GetCategory": "SELECT category_link FROM crawper.categories WHERE category_name=%s;",
    "DeleteCategory": "DELETE FROM crawper.categories WHERE category_name=%s;",
    "ExistsCategory": "SELECT EXISTS(SELECT category_name FROM crawper.categories WHERE "
                      "category_name=%s) ",
    "SelectProductLink": "SELECT product_link FROM crawper.products WHERE category_name=%s;",
    "ExistsProduct": "SELECT EXISTS(SELECT product_asin FROM crawper.products WHERE product_asin=%s);"
}
