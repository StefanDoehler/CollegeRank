from bs4 import BeautifulSoup
from urllib2 import Request, urlopen, HTTPError
import re

us_news_url_25 = "http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities"
niche_url_25 = "https://colleges.niche.com/rankings/best-colleges/"
niche_url_50 = ""


def get_html(url):
    permissions = {
        'User-Agent': "Mozilla/5.0",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    req = Request(url, headers=permissions)

    try:
        page = urlopen(req).read()
        return BeautifulSoup(page, "html.parser")
    except HTTPError, e:
        if e.code == 404:     # page not found
            return None
        elif e.code == 403:   # access denied
            return None


def scrape_us_news(url):
    html = get_html(url)

    if html is None:  # deal with bad url requests
        return None

    blocks = html.find_all(name="div", class_="clearfix")
    schools, ranks = [], []

    for block in blocks[::2]:  # beginning with the first block, every other block contains school information
        schools.append(block.find('h3').find('a', href=True).string)
        ranks.append(re.search(r"#\d*", str(block)).group(0)[1:])

    print schools,
    print ranks,


def scrape_niche(url):
    html = get_html(url)

    if html is None:  # deal with bad url requests
        return None

    blocks = html.find_all(name="div", class_="ranking-item__body")
    schools, ranks = [], []

    for block in blocks:
        schools.append(block.find('h3').find('a', href=True).string)
        ranks.append(block.find(name="div", class_="ranking-item__ordinal").string)

    print schools,
    print
    print ranks,


scrape_niche(niche_url)