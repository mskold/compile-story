#!/usr/bin/env bash
# Convenience script. Just call with the name of the story and it figures out correct path for you

PATH_NOVELL="~/Dropbox/_text/_noveller"
PATH_ROMAN="~/Dropox/_text"
DRAFT_DIR="draft"
OUTPUT_PATH="~/Dropbox/Skrivande"

PATH=$PATH_NOVELL

while getopts "r" OPTION
do
  if [ $OPTION == "r" ]; then PATH=$PATH_ROMAN; fi
done

story=${@:$OPTIND:1}

#compile_story.sh -o $OUTPUT_PATH "${PATH}/${story}/${DRAFT_DIR}/"*
test_compile.sh -o $OUTPUT_PATH "${PATH}/${story}/${DRAFT_DIR}"/*
