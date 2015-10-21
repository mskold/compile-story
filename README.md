# compile-story
BASH script to compile markdown files into HTML, PDF, epub, docx and odt.

## Requirements

* BASH
* Pandoc (http://pandoc.org)
* wkhtmltopdf (http://wkhtmltopdf.org/)

## About

The script takes two arguments.
The first is the output directory, into where the compiled files will go.
The second is the draft diretory – the directory containing the markdown files to be assembled into complete documents.

### Files

The script handles two kinds of files:

1. Metadata
2. Story

Typically, a draft has at most one metadata file and one or more story files. The storyfiles are concatenated into one big file before transformation into other formats.

The metadata file can reside outside (parallell) with the draft directory, or inside it. If it's outside, the metadata file should be named metadata.md, while if it is inside the draft directory, it should be named 00-metadata.md

The metadata can contain information such as the title of the story, the author, revision, language, etc. This information is then used by tools such as pandoc to set metadata about the compiled documents.

The story files will be treated as scenes in the story and thus concatenated with SCENE\_LEVEL (####) and SCENE\_DIVIDER (· · ·) between each file.

### Directories

Directories inside the draft folder will be treated as chapters in the story, using the name of the directory from position 3 (enabling using directory name as sorting for the chapters).

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

### Usage

    $ compile_story.sh /tmp/output ~/path/to/draft

## Other scrips

There are other scripts in this repository as well.

* downdraft.py is a small python application that downloads a directory (typically containing a markdown draft) from dropbox.

* updraft.py uploads compiled files into dropbox.

* cs.sh is a conveniance script for my own setup, that downloads a draft from dropbox, executes the compile\_story-script and uploads all the resulting documents back into dropbox.

### Regarding updraft and downdraft

The scripts require a Dropbox access key to work. You need to register one of these yourself, using the Dropbox API. 

When you have access keys, you just copy the file config.py.in to config.py and update it with your keys.


