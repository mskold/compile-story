# compile_story.sh

BASH script to compile markdown files into HTML, PDF, epub, docx and odt.

# assemble_markdown.sh

BASH script to assemble a tree structure of markdown files into one file.

## Requirements

* BASH
* Pandoc (http://pandoc.org)
* wkhtmltopdf (http://wkhtmltopdf.org/)

## About

There are two scripts at work here. If you write your stories in one single markdown file, you will only need the compile\_story.sh-script
which compiles HTML, EPUB, DOCX, ODT and PDF from a master Markdown file.

The compile-script takes one argument: the name of the markdown-file. The compiled files will end up in the same directory as the markdown file.

The assemble\_markdown script takes two arguments.
The first is the output directory, into where the assembled file will go.
The second is the draft diretory – the directory containing the markdown files to be assembled into one document.

### Files

The assembly script handles two kinds of files:

1. Metadata
2. Story

Typically, a draft has at most one metadata file and one or more story files.

The metadata file can reside outside (parallell) with the draft directory, or inside it. If it's outside, the metadata file should be named metadata.md, while if it is inside the draft directory, it should be named 00-metadata.md

The metadata can contain information such as the title of the story, the author, revision, language, etc. This information is then used by tools such as pandoc to set metadata about the compiled documents.

The story files will be treated as scenes in the story and thus concatenated with SCENE\_LEVEL (####) and SCENE\_DIVIDER (· · ·) between each file.

### Directories

Directories containing markdown files will be treated as chapters in the story. Directories containing other directories will be treated as parts
using the name of the directory from after the first occurrence of a hyphen character as the part name (e.g. "001-Part One/" => "## Part One")

#### Examples

* A short story (without chapters) with the metadata outside the draft folder.

```
StoryDirectory/
    metadata.md
    draft/
        01-a scene.md
        02-another scene.md
        03-the end.md
```

* A short story (without chapters) with the metadata inside the draft folder.

```
AnotherStoryDirectory/
    draft/
        00-metadata.md
        01-introductory scene.md
        02-the middle.md
        03-an explosive ending.md
```

* A longer story (with chapters)

```
MyBook/
    draft/
        00-metadata.md
        01-prologue.md
        02-Chapter 1/
            01-once upon a time.md
            02-scene.md
        03-Chapter 2/
            01-another scene.md

.... etc
```

* An even longer story (with parts and chapters)

```
MyOpus/
    draft/
        00-metadata.md
        01-prologue.md
        02-Part One/
            01-Chapter 1/
                01-once upon a time.md
                02-scene.md
            02-Chapter 2/
                01-another scene.md
        03-Part Two/
            01-Chapter 3/
                01-twice upon a time.md
                02-scene.md
            02-Chapter 4/
                01-another scene.md

.... etc
```

##### Note

If you feel that naming of chapters (i.e. by the dir name after hyphen) is tedious, you can set the parameter ChapterPrefix in 00-metadata.md to use automatic numbering of chapters.

```
title: My story
author: You
chapterPrefix: Chapter
```

This will result in chapters being named Chapter 1, Chapter 2, Chapter 3, etc.

### Usage

    $ assemble_markdown.sh /tmp/output ~/path/to/draft
    $ compile_story.sh /tmp/output/my_assembled_draft.md

## Other scrips

There are other scripts in this repository as well.

* downdraft.py is a small python application that downloads a directory (typically containing a markdown draft) from dropbox.

* updraft.py uploads compiled files into dropbox.

* cs.sh is a conveniance script for my own setup, that downloads a draft from dropbox, executes the compile\_story-script and uploads all the resulting documents back into dropbox.

### Regarding updraft and downdraft

The scripts require a Dropbox access key to work. You need to register one of these yourself, using the Dropbox API. 

When you have access keys, you just copy the file config.py.in to config.py and update it with your keys.


