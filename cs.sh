#!/usr/bin/env bash
# Convenience script. Just call with the name of the story and it figures out correct path for you

PATH_NOVELL="${HOME}/Dropbox/_text/_noveller"
PATH_ROMAN="${HOME}/Dropox/_text"
DRAFT_DIR="draft"
OUTPUT_PATH="${HOME}/Dropbox/_text/_output"

STORY_PATH=$PATH_NOVELL

while getopts "r" OPTION
do
  if [ $OPTION == "r" ]; then STORY_PATH=$PATH_ROMAN; fi
done

story=${@:$OPTIND:1}

export PATH="${PATH}:."

compile_story.sh $OUTPUT_PATH "${STORY_PATH}/${story}/${DRAFT_DIR}"
