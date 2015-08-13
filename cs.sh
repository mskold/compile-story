#!/usr/bin/env bash
# Convenience script.

OUTPUT_PATH="/tmp/cs/output"
DRAFT_PATH="/tmp/cs/draft"

export PATH="${PATH}:."
export PYTHONIOENCODING="UTF-8"

rm -fr "$DRAFT_PATH"
rm -fr "$OUTPUT_PATH"

python downdraft.py "$1"

compile_story.sh $OUTPUT_PATH $DRAFT_PATH

python updraft.py "$1"
