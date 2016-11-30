from bs4 import BeautifulSoup
from urllib2 import Request, urlopen, HTTPError
import re

us_news_url_25 = "http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities"
niche_url_25 = "https://colleges.niche.com/rankings/best-colleges/"
best_colleges_url_50 = "http://www.thebestcolleges.org/rankings/top-50/"
best_schools_url_50 = "http://www.thebestschools.org/features/100-best-universities-in-world-today/"


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

    print "****" + "US NEWS" + "*"*20
    print schools,
    print
    print ranks,
    print


def scrape_niche(url):
    html = get_html(url)

    if html is None:  # deal with bad url requests
        return None

    blocks = html.find_all(name="div", class_="ranking-item__body")
    schools, ranks = [], []
    rank = 1

    for block in blocks:
        schools.append(block.find("h3").find("a", href=True).string)
        ranks.append(rank)
        rank += 1

    print "****" + "NICHE" + "*" * 25
    print schools,
    print
    print ranks,
    print


def scrape_best_colleges(url):
    html = get_html(url)

    if html is None:  # deal with bad url requests
        return None

    chunk = html.find(name="ol", class_="directory-links")
    blocks = chunk.find_all("li")
    schools, ranks = [], []
    rank = 1

    for block in blocks:
        header = block.find("h4")

        if header is None:
            continue

        schools.append(header.find("a", href=True).string)
        ranks.append(rank)
        rank += 1

    print "****" + "BEST COLLEGES" + "*" * 15
    print schools,
    print
    print ranks,
    print


def scrape_best_schools(url):
    html = get_html(url)

    if html is None:  # deal with bad url requests
        return None

    blocks = html.find_all(name="h3", class_="college")
    schools, ranks, locations = [], [], []

    for block in blocks:
        location = block.find_next_sibling().contents[1]
        if "USA" not in location:
            continue
        schools.append(block.contents[1])
        ranks.append(block.find("span").string)
        locations.append(location)

    print "****" + "BEST SCHOOLS" + "*" * 15
    print schools,
    print
    print ranks,
    print
    print locations,
    print


#scrape_us_news(us_news_url_25)
#scrape_niche(niche_url_25)
#scrape_best_colleges(best_colleges_url_50)
scrape_best_schools(best_schools_url_50)