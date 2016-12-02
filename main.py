from bs4 import BeautifulSoup
from urllib2 import Request, urlopen, HTTPError
import re


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
    result = {}

    for block in blocks[::2]:  # beginning with the first block, every other block contains school information
        school = block.find("h3").find("a", href=True).string
        rank = re.search(r"#\d*", str(block)).group(0)[1:]
        location = block.find(name="div", class_="block-normal text-small").text
        result[school] = [rank, location]

    return result


def scrape_niche(url):
    html = get_html(url)

    if html is None:  # deal with bad url requests
        return None

    blocks = html.find_all(name="div", class_="ranking-item__body")
    result = {}
    rank = 1

    for block in blocks:
        school = block.find("h3").find("a", href=True).string
        location = block.find(name="li", class_="ranking-item__entity__tagline__item").text
        result[school] = [rank, location]
        rank += 1

    return result


def scrape_best_colleges(url):
    html = get_html(url)

    if html is None:  # deal with bad url requests
        return None

    chunk = html.find(name="ol", class_="directory-links")
    blocks = chunk.find_all("li")
    result = {}
    rank = 1

    for block in blocks:
        header = block.find("h4")

        if header is None:  # not all blocks contain school names
            continue

        school = header.find("a", href=True).string
        location = block.find("strong").text
        result[school] = [rank, location]
        rank += 1

    return result


def scrape_best_schools(url):
    html = get_html(url)

    if html is None:  # deal with bad url requests
        return None

    blocks = html.find_all(name="h3", class_="college")
    result = {}
    rank = 1

    for block in blocks:
        location = block.find_next_sibling().contents[1]

        if "USA" not in location:  # do not include schools outside the US
            continue

        school = block.contents[1]
        location = location[1:-6]  # remove "(" at beginning and ", USA" at end
        result[school] = [rank, location]
        rank += 1

    return result


def scrape_college_raptor(url):
    html = get_html(url)

    if html is None:  # deal with bad url requests
        return None

    blocks = html.find_all(name="h2")
    result = {}
    rank = 50

    for block in blocks:
        splice = 4 if rank >= 10 else 3
        school = block.text[splice:]
        location = block.find_next_sibling().find_next_sibling().text
        result[school] = [rank, location]
        rank -= 1

    return result
