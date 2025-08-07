import sys
import os
import pytest
import json
from bs4 import BeautifulSoup
from sites.purrfectcompanions.parser import parse_profile_page

def test_parse_profile_page():
    with open("tests/purrfectcompanions/profilepage.html", "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    result = parse_profile_page(soup)

    print(json.dumps(result, indent=2))