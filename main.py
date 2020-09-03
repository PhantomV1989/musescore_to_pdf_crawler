import requests
from pyquery import PyQuery as pq
import os
from PyPDF2 import PdfFileMerger

s = "https://musescore.com/shadowtenshii/ocarina-of-time---gerudo-valley-piano-transcription"

object = requests.get(s)
body = object.text
b1 = pq(body)
title = b1('title')[0].text.split(' | ')[0]

if not os.path.exists(title):
    os.mkdir(title)

type = 'svg'
pos = body.find('/score_0.' + type + '?no-cache=')
if pos > -1:
    start = pos - 1
    end = pos + 1
    for i in range(pos, 0, -1):
        if body[i] == '"' or body[i] == ';':
            start = i + 1
            break

    for i in range(pos, len(body), 1):
        if body[i] == '"' or body[i] == ';':
            end = i
            break
else:
    type = 'png'
    pos = body.find('/score_0.' + type + '?no-cache=')
    start = pos - 1
    end = pos + 1
    for i in range(pos, 0, -1):
        if body[i] == '"' or body[i] == ';':
            start = i + 1
            break

    end = pos + 12
if pos == -1:
    raise Exception('New file type')
l = body[start:end]
page = 0
last = 'score_0'
merger = PdfFileMerger()
f1 = []
while True:
    current = "score_" + str(page)
    l = l.replace(last, current)
    r = requests.get(l)
    if r.status_code > 200:
        break
    fpath = title + '/' + current + '.' + type
    with open(fpath, 'wb') as f:
        f.write(r.content)
        f1.append(fpath)
    page += 1
    last = current

if type == 'svg':
    import cairosvg

    for fpath in f1:
        fpathPdf = title + '/' + fpath[-5] + '.pdf'
        cairosvg.svg2pdf(file_obj=open(fpath, "rb"), write_to=fpathPdf)
        merger.append(open(fpathPdf, 'rb'))

    with open(title + ".pdf", "wb") as f:
        merger.write(f)
if type == "png":
    import img2pdf
    with open(title + ".pdf", "wb") as f:
        try:
            f.write(img2pdf.convert(f1))
        except:
            from PIL import Image

            for fpath in f1:
                png = Image.open(fpath)
                png.load()  # required for png.split()

                background = Image.new("RGB", png.size, (255, 255, 255))
                background.paste(png, mask=png.split()[3])  # 3 is the alpha channel

                background.save(fpath, 'PNG', quality=80)
            f.write(img2pdf.convert(f1))

import shutil

shutil.rmtree(title)
# https://musescore.com/static/musescore/scoredata/gen/8/3/2/5664238/72c702cefe8620cdd83ecdf13a615481ac83e39f/score_0.svg?no-cache=1564883164
