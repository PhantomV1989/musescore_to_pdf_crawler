import requests
from pyquery import PyQuery as pq
import os
import cairosvg
from PyPDF2 import PdfFileMerger

s = "https://musescore.com/user/27888658/scores/5664238"


default_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers'
}

object = requests.get(s, headers=default_headers)
body = object.text
b1 = pq(body)
title = b1('title')[0].text.split(' | ')[0]

if not os.path.exists(title):
    os.mkdir(title)

pos = body.find('/score_0.svg?no-cache=')
start = pos - 1
end = pos + 1
for i in range(pos, 0, -1):
    if body[i] == '"':
        start = i + 1
        break

for i in range(pos, len(body), 1):
    if body[i] == '"':
        end = i
        break
l = body[start:end]
page = 0
last = 'score_0'
merger = PdfFileMerger()
dlist = []
while True:
    current = "score_" + str(page)
    l = l.replace(last, current)
    r = requests.get(l, headers=default_headers)
    if r.status_code > 200:
        break
    fpath = title + '/' + current + '.svg'
    with open(fpath, 'w') as f:
        f.write(r.text)
        fpathPdf = title + '/' + current + '.pdf'
        cairosvg.svg2pdf(file_obj=open(fpath, "rb"), write_to=title + '/' + current + '.pdf')
        merger.append(open(fpathPdf, 'rb'))
    page += 1
    last = current
with open(title + ".pdf", "wb") as f:
    merger.write(f)

import shutil
shutil.rmtree(title)
# https://musescore.com/static/musescore/scoredata/gen/8/3/2/5664238/72c702cefe8620cdd83ecdf13a615481ac83e39f/score_0.svg?no-cache=1564883164
