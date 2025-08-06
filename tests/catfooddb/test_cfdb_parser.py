import sys
import os
import pytest
from bs4 import BeautifulSoup
from crawlers.catfooddb.parser import parse_review_links


def test_parse_review_links():
    html = """
        <html>
            <body>
                <a href="product/one">
                    <button class="btn btn-review">Review 1</button>
                </a>
                <a href="product/two">
                    <button class="btn btn-review">Review 2</button>
                </a>
                <a href="product/three">
                    <button class="btn other-class">Not a review</button>
                </a>
                <a href="product/four">
                    <button class="btn btn-review">Review 4</button>
                </a>
            </body>
        </html>
    """

    soup = BeautifulSoup(html, "html.parser")
    current_url = "https://catfooddb.com/brand/xyz"

    result = parse_review_links(soup, current_url)

    expected = [
        "https://catfooddb.com/brand/product/one",
        "https://catfooddb.com/brand/product/product/two",
        "https://catfooddb.com/brand/product/product/product/four",
    ]
    assert result == expected
