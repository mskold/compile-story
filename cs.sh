#!/usr/bin/env bash
# Convenience script.

OUTPUT_PATH="/tmp/cs/output"
DRAFT_PATH="/tmp/cs/draft"

export PATH="${PATH}:."
export PYTHONIOENCODING="UTF-8"

rm -fr "$DRAFT_PATH"
rm -fr "$OUTPUT_PATH"

SCRIPT_PATH=`dirname $0`

python ${SCRIPT_PATH}/downdraft.py "$1"

assemble_markdown.sh $OUTPUT_PATH $DRAFT_PATH

markdown_file="${OUTPUT_PATH}/$(ls ${OUTPUT_PATH})"
compile_story.sh "$markdown_file"

python ${SCRIPT_PATH}/updraft.py "$1"
