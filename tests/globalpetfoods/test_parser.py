import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from bs4 import BeautifulSoup
from crawlers.globalpetfoods.parser import parse_next_page

def test_parse_next_page():
	html = """
	<html>
		<body>
			<!-- PAGINATION -->
			<div class="cuctom-pagin">
				<div class="pull-left">
					<span class="endless_page_current">
					<strong>1</strong>
					</span>
					<a href="/products/list/?categories=0004&amp;page=2"
					data-el-querystring-key="page"
					class="endless_page_link">2</a>
					<a href="/products/list/?categories=0004&amp;page=3"
					data-el-querystring-key="page"
					class="endless_page_link">3</a>
					<span class="endless_separator">...</span>
					<a href="/products/list/?categories=0004&amp;page=6"
					data-el-querystring-key="page"
					class="endless_page_link">6</a>
					<a href="/products/list/?categories=0004&amp;page=7"
					data-el-querystring-key="page"
					class="endless_page_link">7</a>
					<a href="/products/list/?categories=0004&amp;page=8"
					data-el-querystring-key="page"
					class="endless_page_link">8</a>
					<a href="/products/list/?categories=0004&amp;page=2"
					data-el-querystring-key="page"
					class="endless_page_link">Next</a>
				</div>
				<span tabindex="0" class="show-count-prdct pull-right">Showing entries
				1-45 of
				328.</span>
				<div class="clearfix"></div>
			</div>
			<!-- PAGINATION -->
		</body>
	</html>
	"""
	soup = BeautifulSoup(html, "html.parser")
	current_url = "https://brantford.globalpetfoods.com/products/list/?page=1&categories=0004"

	result = parse_next_page(soup, current_url)

	assert result == "https://brantford.globalpetfoods.com/products/list/?categories=0004&page=2"

def test_parse_next_page_no_pagination():
	html = """
	<html>
		<body>
			<!-- PAGINATION -->
			<div class="cuctom-pagin">
				<div class="pull-left">
					<span class="endless_page_current">
					<strong>1</strong>
					</span>
					<a href="/products/list/?categories=0004&amp;page=2"
					data-el-querystring-key="page"
					class="endless_page_link">2</a>
					<a href="/products/list/?categories=0004&amp;page=3"
					data-el-querystring-key="page"
					class="endless_page_link">3</a>
					<span class="endless_separator">...</span>
					<a href="/products/list/?categories=0004&amp;page=6"
					data-el-querystring-key="page"
					class="endless_page_link">6</a>
					<a href="/products/list/?categories=0004&amp;page=7"
					data-el-querystring-key="page"
					class="endless_page_link">7</a>
					<a href="/products/list/?categories=0004&amp;page=8"
					data-el-querystring-key="page"
					class="endless_page_link">8</a>
				</div>
				<span tabindex="0" class="show-count-prdct pull-right">Showing entries
				1-45 of
				328.</span>
				<div class="clearfix"></div>
			</div>
			<!-- PAGINATION -->
		</body>
	</html>
	"""
	soup = BeautifulSoup(html, "html.parser")
	current_url = "https://brantford.globalpetfoods.com/products/list/?page=1&categories=0004"

	result = parse_next_page(soup, current_url)

	assert result == None