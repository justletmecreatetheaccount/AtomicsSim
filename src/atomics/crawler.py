import os
import re
import time
import requests
from bs4 import BeautifulSoup

BASE = "https://wwwndc.jaea.go.jp/cgi-bin/nucltab14?"
OUT = "data/nuC_pages"
os.makedirs(OUT, exist_ok=True)

session = requests.Session()
session.headers["User-Agent"] = "student-homework-script vlad.doniga@student.uclouvain.be"


pages = {}
for i in range(0, 119):
    url = format(BASE + i.__str__())
    print(url)
    html = session.get(url, timeout=30).text
    pages[url] = html
    time.sleep(1)          # be polite: ~1 page/sec max
    path = format(OUT + "/Element" + i.__str__() + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    
