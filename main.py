from bs4 import BeautifulSoup
from urllib2 import Request, urlopen
import re

url = "http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities"
headers = {
    'User-Agent': "Mozilla/5.0",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
req = Request(url, headers=headers)
page = urlopen(req).read()
html = BeautifulSoup(page, "html.parser")
blocks = html.find_all("div", class_="clearfix")
for block in blocks[::2]:
    school = block.find('h3').find('a', href=True).string
    num = re.search(r"#\d*", str(block)).group(0)[1:]
    print "name:",
    print school
    print "num:",
    print num