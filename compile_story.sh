#!/usr/bin/env bash

BASE_OUTPUT_DIR="/Users/markus/Dropbox/Skrivande/_kompilerat/"


#if [[ -t 0 ]]; then
    # Running with filename as argument
MARKDOWN_DRAFT="$1"
#STORY_NAME="$(basename "$1" .md)"
#else
#    # Running through a pipe, write markdown draft to /tmp/markdown_draft.md
#    echo "" > /tmp/markdown_draft.md
#    while read line; do
#        echo "${line}" >> /tmp/markdown_draft.md
#    done < /dev/stdin
#    MARKDOWN_DRAFT="/tmp/markdown_draft.md"
#fi

if [ ! -f "$MARKDOWN_DRAFT" ]; then
    echo "Draft file \"${MARKDOWN_DRAFT}\" does not exist."
    exit 1
fi

function realpath() {
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

CSS=$(realpath `dirname "$0"`"/style/manuscript.css")
DOCXREF=$(realpath `dirname "$0"`"/style/reference.docx")
ODTREF=$(realpath `dirname "$0"`"/style/reference.odt")

#OUTPUT_DIR=$(realpath `dirname "$MARKDOWN_DRAFT"`)

PANDOC="pandoc"
WKHTML2PDF="wkhtmltopdf"
# I needed to wrap wkhtmltopdf in a script calling it with xvfb-run when on a headless linux box
#WKHTML2PDF="wkhtml2pdf.sh"

# Get parameters from markdown file
title=`grep -i "^Title: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`
revision=`grep -i "^Revision: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`
file_title=`grep -i "^ShortTitle: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`
author=`grep -i "^Author: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`
series=`grep -i "^Series: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`
series_index=`grep -i "^SeriesIndex: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`
tags=`grep -i "^Tags: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`
cover=`grep -i "^Cover: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`
language=`grep -i "^Language: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`
draftlevel=`grep -i "^DraftLevel: " "${MARKDOWN_DRAFT}" |awk -F ': ' '{print $2}'`

if [ "$file_title" == "" ]; then
    file_title="${title}"
    # If no title is found, assume it's a story section
    if [ "$file_title" = "" ]; then
        file_title="selected"
    fi
fi
if [ "$language" == "" ]; then
    language="swedish"
fi
if [ "$draftlevel" == "final" ]; then
    # If draftlevel is final, prepare a complete file name, ready for submission
    file_title="$(echo -n "${file_title}-${author}" | tr -s " " "_")"
elif [ "$revision" != "" ]; then
    file_title="${file_title}-${revision}"
fi
if [ "$draftlevel" == "draft" ]; then
    file_title="$file_title (utkast)"
fi
if [ "$draftlevel" == "proof" ]; then
    file_title="$file_title (korrektur)"
fi

OUTPUT_DIR="${BASE_OUTPUT_DIR}/${title}"

echo "OUTPUT_DIR: $OUTPUT_DIR"
mkdir -p "${OUTPUT_DIR}"

smart=""
# The "smart"-flag causes quotes to be created with english style (i.e. inverted starting quote)
if [ "$language" == "english" ]; then
    smart="--smart"
fi

echo "Creating HTML"
$PANDOC -V lang=$language $smart -s -t html -c $CSS -o "${OUTPUT_DIR}/${file_title}.html" "${MARKDOWN_DRAFT}"

echo "Compiling PDF"
$WKHTML2PDF --margin-top 20 --margin-bottom 20 --margin-right 30 --margin-left 30 --page-size A4 --encoding utf-8 --footer-font-name "Times New Roman" --footer-spacing 10 --header-font-name "Times New Roman" --header-font-size 9 --header-spacing 10 --header-right "$title / $author" --footer-center "[page]" "${OUTPUT_DIR}/${file_title}.html" "${OUTPUT_DIR}/${file_title}.pdf"

#echo "Compiling MOBI"
#$EBOOKCONVERT "${OUTPUT_DIR}/${file_title}.html" "${OUTPUT_DIR}/$short_title.mobi" --authors="$author" --series="$series" --series-index=$series_index --title="$title" --tags="$tags" --output-profile=kindle

echo "Compiling EPUB"
$PANDOC -V lang=$language $smart -t epub --epub-stylesheet=$CSS --epub-chapter-level=3 -o "${OUTPUT_DIR}/${file_title}.epub" "${MARKDOWN_DRAFT}"

echo "Compiling DOCX"
$PANDOC -V lang=$language $smart -t docx --reference-docx ${DOCXREF} -o "${OUTPUT_DIR}/${file_title}.docx" "${MARKDOWN_DRAFT}"

echo "Compiling ODT"
$PANDOC -V lang=$language $smart -t odt --reference-odt ${ODTREF} -o "${OUTPUT_DIR}/${file_title}.odt" "${MARKDOWN_DRAFT}"
