#!/usr/bin/env bash

# Deprecated. Use assemble_draft.py instead.

OUTPUT_DIR="$1"
DRAFT_DIR="$2"

if [ ! -d "$DRAFT_DIR" ]; then
    echo "Draft directory \"${DRAFT_DIR}\" does not exist."
    exit 1
fi

function realpath() {
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

CSS=$(realpath `dirname "$0"`"/style/manuscript.css")
DOCXREF=$(realpath `dirname "$0"`"/style/reference.docx")
ODTREF=$(realpath `dirname "$0"`"/style/reference.odt")

PART_LEVEL="##"
CHAPTER_LEVEL="###"
SCENE_LEVEL="####"
SCENE_DIVIDER="· · ·"
SCENE_DIVIDER_REPLACE_MARK="***"

METADATAFILE="${DRAFT_DIR}/00-metadata.md"
metadataoutsidedraft="false"

if [ ! -f "${METADATAFILE}" ]; then
    echo "Metadatafile ${METADATAFILE} not found in ${DRAFT_DIR}."
    METADATAFILE="${DRAFT_DIR}/../metadata.md"
    if [ -f ${METADATAFILE} ]; then
      metadataoutsidedraft="true"
    fi
fi

if [ ! -f "${METADATAFILE}" ]; then
    echo "Metadatafile ${METADATAFILE} does not exist. Assuming StoryPart ..."
    file_title="selected"
else
    # Get parameters from metadata file
    title=`grep -i "^Title: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
    file_title=`grep -i "^ShortTitle: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
    language=`grep -i "^Language: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
    scene_divider=`grep -i "^SceneDivider: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
    chapter_prefix=`grep -i "^ChapterPrefix: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
    story_type=`grep -i "^StoryType: " "${METADATAFILE}" |awk -F ': ' '{print $2}'`
fi

if [ "$scene_divider" != "" ]; then
    SCENE_DIVIDER="$scene_divider"
fi
if [ "$file_title" == "" ]; then
    file_title="${title}"
fi

part_structure="false"

dir_depth() {
    cd "$@"
    maxdepth=0
    for d in */.; do
        [ -d "$d" ] || continue
        depth=`dir_depth "$d"`
        maxdepth=$(($depth > $maxdepth ? $depth : $maxdepth))
    done
    echo $((1+maxdepth))
}

manuscript_depth=$(dir_depth "${DRAFT_DIR}")

if [ $manuscript_depth -ge 2 ]; then
    # Directory depth indicates a manuscript with parts
    part_structure="true"
    echo "Setting part structure"
fi

mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${file_title}.md"

if [ $metadataoutsidedraft == "true" ]; then
    # Append metadata.md as YAML section in master markdown file
    # (This enables pandoc to add metadata to generated documents, such as Author and Title)
    echo "---" > "$OUTPUT_FILE"
    cat "${METADATAFILE}" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

chapter_number=1

function concat_story() {
    first_markdown_file_in_directory="true"
    depth=$1
    for file in "${@:2}"; do
        bnamech=`basename "$file"`
        # Find position of dash in directory name
        dash_position=0
        tmp="${bnamech%%-*}"
        if [ "$tmp" != "$bnamech" ]; then
            dash_position=$((${#tmp}+1))
        fi
        section="${bnamech:$dash_position}"
        if [ -d "$file" ]; then
            depth=$((depth+1))
            echo "" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            #if [ "$part_structure" == "false" ] || [ $depth -eq 2 ]; then
            #    if [ "$chapter_prefix" != "" ]; then
            #        echo "${CHAPTER_LEVEL} ${chapter_prefix} ${chapter_number}" >> "$OUTPUT_FILE"
            #        chapter_number=$((chapter_number+1))
            #    else
            #        echo "${CHAPTER_LEVEL} ${section}" >> "$OUTPUT_FILE"
            #    fi
            #else
            echo "${PART_LEVEL} ${section}" >> "$OUTPUT_FILE"
            #fi
            echo "" >> "$OUTPUT_FILE"
            concat_story $depth "$file"/*
            depth=$((depth-1))
        else
            # Breath some space into output file
            echo "" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            if head -1 "$file" |grep -q "^#"; then
                first_markdown_file_in_directory="true"
            fi
            if [ "$(basename "$file")" == "00-metadata.md" ]; then
                first_markdown_file_in_directory="true"
                # Append metadata.md as YAML section in master markdown file
                # (This enables pandoc to add metadata to generated documents, such as Author and Title)
                echo "---" > "$OUTPUT_FILE"
                cat "$file" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
                echo "---" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
            else
                if [ "$story_type" == "Novel" ]; then
                    if [ "$chapter_prefix" != "" ]; then
                        echo "${CHAPTER_LEVEL} ${chapter_prefix} ${chapter_number}" >> "$OUTPUT_FILE"
                        chapter_number=$((chapter_number+1))
                    else
                        echo "${CHAPTER_LEVEL} ${section}" >> "$OUTPUT_FILE"
                    fi
                elif [ "$first_markdown_file_in_directory" == "false" ]; then
                        echo "${SCENE_LEVEL} ${SCENE_DIVIDER}" >> "$OUTPUT_FILE"
                fi
                echo "" >> "$OUTPUT_FILE"
                cat "$file" >> "$OUTPUT_FILE"
                first_markdown_file_in_directory="false"
            fi
        fi
    done
}

# Concatenate all markdown files into the master markdown file.
# (Folders are treated as parts and chapters, with the directory name (from position 3) as the chapter name (with heading level $PART_LEVEL & $CHAPTER_LEVEL).
# Individual markdown files in each directory are concatenated with a $SCENE_DIVIDER as separator (with heading level $SCENE_LEVEL)
concat_story 0 "${DRAFT_DIR}"/*

# Replace scene mark with configured scene divider.
sed -i.sed "s/\*\*\*/${SCENE_LEVEL} ${SCENE_DIVIDER}/" "$OUTPUT_FILE" && rm "${OUTPUT_FILE}.sed"
# Replace double dash with en-dash
sed -i.sed 's/ -- / – /g' "$OUTPUT_FILE" && rm "${OUTPUT_FILE}.sed"
# Remove trailing whitespace (yes, i think the "double space linebreak" is an abomination in markdown).
sed -i.sed 's/[ ]*$//' "$OUTPUT_FILE" && rm "${OUTPUT_FILE}.sed"
# If not left to the compiler, replace all quotes in the master markdown file with typographic quotes.
# TODO: Need if here? Why not always?
if [ "$language" != "english" ]; then
    sed -i.sed 's/\"/\”/g' "$OUTPUT_FILE" && rm "${OUTPUT_FILE}.sed"
fi
