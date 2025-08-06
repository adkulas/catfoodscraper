import sys
import os
import pytest
from bs4 import BeautifulSoup
from crawlers.catfooddb.parser import parse_review_links


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
    print(result)
    expected = [
        "https://catfooddb.com/product/zoe/P%C3%A2t%C3%A9+With+Free+Run+Chicken",
        "https://catfooddb.com/product/zoe/P%C3%A2t%C3%A9+With+Wild-Caught+Fish",
        "https://catfooddb.com/product/zoe/P%C3%A2t%C3%A9+With+Fresh+Turkey",
    ]
    assert result == expected
