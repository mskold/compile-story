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

compile_story.sh $OUTPUT_PATH $DRAFT_PATH

python ${SCRIPT_PATH}/updraft.py "$1"
