import sys
import os
import pytest
import json
from bs4 import BeautifulSoup
from sites.catfooddb.parser import parse_review_links, parse_product_review


def test_parse_review_links():
    html = """
        <html>
            <body>
                <a href="product/zoe/P%C3%A2t%C3%A9+With+Free+Run+Chicken">
                    <button class="btn btn-review">Review 1</button>
                </a>
                <a href="product/zoe/P%C3%A2t%C3%A9+With+Wild-Caught+Fish">
                    <button class="btn btn-review">Review 2</button>
                </a>
                <a href="product/three">
                    <button class="btn other-class">Not a review</button>
                </a>
                <a href="product/zoe/P%C3%A2t%C3%A9+With+Fresh+Turkey">
                    <button class="btn btn-list-item center-block btn-review buy-now bold" style="width:100%; margin-bottom: 10px">Full CatFoodDB Review</button>
                </a>
            </body>
        </html>
    """

    soup = BeautifulSoup(html, "html.parser")
    current_url = "https://catfooddb.com/brand/zoe"

    result = parse_review_links(soup, current_url)
    expected = [
        "https://catfooddb.com/product/zoe/P%C3%A2t%C3%A9+With+Free+Run+Chicken",
        "https://catfooddb.com/product/zoe/P%C3%A2t%C3%A9+With+Wild-Caught+Fish",
        "https://catfooddb.com/product/zoe/P%C3%A2t%C3%A9+With+Fresh+Turkey",
    ]
    assert result == expected


def test_parse_product_review():
    test_html_path = os.path.join(os.path.dirname(__file__), "review_page.html")
    with open(test_html_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    result = parse_product_review(soup)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    # expected = {
    #     "name": "Pâté With Free Run Chicken",
    #     "brand": "Zoe",
    #     "rating": 4.5,
    #     # ...other expected fields...
    # }
    # assert result == expected