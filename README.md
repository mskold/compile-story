# compile_story.sh

BASH script to compile markdown file into HTML, PDF, epub, docx and odt.

# assemble_draft.py

Python script to assemble a tree structure of markdown files into one file.

## Requirements

* Python
* BASH
* Pandoc (http://pandoc.org)
* wkhtmltopdf (http://wkhtmltopdf.org/)

## About

There are two scripts at work here. If you write your stories in one single markdown file, you will only need the compile\_story.sh-script
which compiles HTML, EPUB, DOCX, ODT and PDF from a master Markdown file.

The compile-script takes one argument: the name of the markdown-file. The compiled files will end up in the same directory as the markdown file.

The assemble\_draft.py script takes one argument: The draft directory, containing the markdown files to be assembled into one document.

### Files

The assembly script handles two kinds of files:

1. Metadata
2. Story

Typically, a draft has at most one metadata file and one or more story files.

The metadata file can reside outside (parallell) with the draft directory, or inside it. If it's outside, the metadata file should be named metadata.md, while if it is inside the draft directory, it should be named 00-metadata.md

The metadata can contain information such as the title of the story, the author, revision, language, etc. This information is then used by tools such as pandoc to set metadata about the compiled documents.

The story files will be treated as scenes in the story and thus concatenated with SCENE\_LEVEL (####) and SCENE\_DIVIDER (· · ·) between each file.

### Directories

Directories will be treated as parts using the name of the directory from after the first occurrence of a hyphen character as the part name (e.g. "001-Part One/" => "## Part One")

### Novels or short stories

Setting the storytype-parameter in the 00-metadata.md impacts how the assembly script treats individual markdown files. If storytype is set to "Novel", each markdown file will be treated as a chapter (i.e. the separator used will be the CHAPTER-separator (###) and an automatic chapter number, with an optional "chapterprefix".

If the storytype is unset (default) or set to "short story", each markdown file will be treated as a scene in the story (the separator will be #### · · ·).

Both chapternames and scene dividers may be overridden by adding a chapter or scenedivider as the first line in the following file.


#### Examples

* A story with the metadata outside the draft folder.

```
StoryDirectory/
    metadata.md
    draft/
        01-a scene.md
        02-another scene.md
        03-the end.md
```

* A story with the metadata inside the draft folder.

```
AnotherStoryDirectory/
    draft/
        00-metadata.md
        01-introductory scene.md
        02-the middle.md
        03-an explosive ending.md
```

* A longer story (with parts)

```
MyBook/
    draft/
        00-metadata.md
        01-prologue.md
        02-Part 1/
            01-once upon a time.md
            02-scene.md
            ...
        03-Part 2/
            01-another scene.md

.... etc
```

### Usage

        $ assemble_draft.py ~/path/to/draft > /tmp/output/my_assembled_draft.md
        $ compile_story.sh /tmp/output/my_assembled_draft.md

## Other scrips

There are other scripts in this repository as well.

* downdraft.py is a small python application that downloads a directory (typically containing a markdown draft) from dropbox.

* updraft.py uploads compiled files into dropbox.

* cs.sh is a conveniance script for my own setup. It downloads a draft from dropbox, executes the compile\_story-script and uploads all the resulting documents back into dropbox.

### Regarding updraft and downdraft

The scripts require a Dropbox access key to work. You need to register one of these yourself, using the Dropbox API.

When you have access keys, you just copy the file config.py.in to config.py and update it with your keys.
