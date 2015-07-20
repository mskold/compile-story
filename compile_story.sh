#!/usr/bin/env bash

#BASE_OUTPUT_DIR="${HOME}/Dropbox/Skrivande"
BASE_OUTPUT_DIR="$1"
DRAFT_DIR="$2"

function realpath() {
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

#CSS="${HOME}/Dropbox/scripts/style/manuscript.css"
CSS=$(realpath "style/manuscript.css")
#DOCXREF="${HOME}/Dropbox/scripts/style/reference.docx"
DOCXREF=$(realpath "style/reference.docx")
#ODTREF="${HOME}/Dropbox/scripts/style/reference.odt"
ODTREF=$(realpath "style/reference.odt")

CHAPTER_LEVEL="###"
SCENE_LEVEL="####"
SCENE_DIVIDER="· · ·"

PANDOC="pandoc"
WKHTML2PDF="wkhtmltopdf"
# I needed to wrap wkhtmltopdf in a script calling it with xvfb-run when on a headless linux box
WKHTML2PDF="wkhtml2pdf.sh"

#METADATAFILE=`dirname "$1"`"/../metadata.md"
METADATAFILE="${DRAFT_DIR}/../metadata.md"

# Get parameters from metadata file
title=`grep "^Title: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
revision=`grep "^Revision: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
short_title=`grep "^ShortTitle: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
author=`grep "^Author: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
series=`grep "^Series: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
series_index=`grep "^SeriesIndex: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
tags=`grep "^Tags: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
cover=`grep "^Cover: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
language=`grep "^Language: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
storytype=`grep "^StoryType: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
draftlevel=`grep "^DraftLevel: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`

# Short title can be used if I want to control the final file name. Otherwise, just use $title.
if [ "$short_title" == "" ]; then
    short_title="${title}"
fi
# If draftlevel is final, prepare a complete file name, ready for submission
if [ "$draftlevel" == "final" ]; then
    short_title="$(echo -n "${short_title}-${author}" | tr -s " " "_")"
fi
if [ "$revision" != "" ]; then
    short_title="${short_title}-rev${revision}"
fi
if [ "$draftlevel" == "draft" ]; then
    short_title="$short_title (utkast)"
fi
if [ "$draftlevel" == "proof" ]; then
    short_title="$short_title (korrektur)"
fi

epub_chapter_level=""

# Set and create output directory
if [ "$storytype" == "Novel" ];
then
    OUTPUT_DIR="${BASE_OUTPUT_DIR}/Romaner/$(date +%Y)/${short_title}/$(date +%Y%m%d)"
    # This causes pandoc to force a page break for each chapter, and isn't necessary in a short story
    epub_chapter_level="--epub-chapter-level=3"
else
    OUTPUT_DIR="${BASE_OUTPUT_DIR}/Noveller/$(date +%Y)/${short_title}/$(date +%Y%m%d)"
fi

mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${short_title}.md"

# Append metadata.md as YAML section in master markdown file
# (This enables pandoc to add metadata to generated documents, such as Author and Title)
echo "---" > "$OUTPUT_FILE"
cat "${METADATAFILE}" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

function concat_story() {
    first="true"
    for file in "$@"; do
        if [ -d "$file" ]; then
            bnamech=`basename "$file"`
            chapter="${bnamech:3}"
            echo "" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo "${CHAPTER_LEVEL} ${chapter}" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            concat_story "$file"/*
        else
            if head -1 "$file" |grep -q "^#### "; then
                first="true"
                # Breath some space into output file
                echo "" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
            fi
            if [ "$first" == "false" ];then
                echo "Inserting divider · between scenes."
                echo "" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
                echo "${SCENE_LEVEL} ${SCENE_DIVIDER}" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
            fi
            echo "Concatenating storyfile ${file} to output ... "
            cat "$file" >> "$OUTPUT_FILE"
            first="false"
        fi
    done
}

# Concatenate all markdown files into the master markdown file.
# (Folders are treated as chapters, with the directory name (from position 3) as the chapter name (with heading level 3).
# Individual markdown files in each directory are concatenated with a · as separator (with heading level 4)
concat_story "${DRAFT_DIR}"/*

# The "smart"-flag causes quotes to be created with english style (i.e. inverted starting quote)
smart=""

if [ "$language" == "english" ]; then
    smart="--smart"
else
    # If not left to the compiler, replace all quotes in the master markdown file with typographic quotes.
    sed -i.sed 's/\"/\”/g' "$OUTPUT_FILE" && rm "${OUTPUT_FILE}.sed"
fi

echo "Creating HTML"
$PANDOC $smart -s -t html -c $CSS -o "${OUTPUT_DIR}/${short_title}.html" "${OUTPUT_DIR}/${short_title}.md"

echo "Compiling PDF"
$WKHTML2PDF "${OUTPUT_DIR}/${short_title}.html" "${OUTPUT_DIR}/${short_title}.pdf"

#echo "Compiling MOBI"
#$EBOOKCONVERT "${OUTPUT_DIR}/${short_title}.html" "${OUTPUT_DIR}/$short_title.mobi" --authors="$author" --series="$series" --series-index=$series_index --title="$title" --tags="$tags" --output-profile=kindle

echo "Compiling EPUB"
$PANDOC -t epub --epub-stylesheet=$CSS $epub_chapter_level -o "${OUTPUT_DIR}/${short_title}.epub" "${OUTPUT_DIR}/${short_title}.md"

echo "Compiling DOCX"
$PANDOC -t docx --reference-docx ${DOCXREF} -o "${OUTPUT_DIR}/${short_title}.docx" "${OUTPUT_DIR}/${short_title}.md"

echo "Compiling ODT"
$PANDOC -t odt --reference-odt ${ODTREF} -o "${OUTPUT_DIR}/${short_title}.odt" "${OUTPUT_DIR}/${short_title}.md"
