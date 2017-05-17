#!/usr/bin/env bash

MANUSCRIPT=$1
COVER=$2

pandoc -V lang=sv -t epub --template=style/pandoc_epub_template.html --epub-stylesheet=style/epub_style.css  --epub-cover-image=${COVER}  -o book.epub metadata.yaml "${MANUSCRIPT}"
