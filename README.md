# compile-story
BASH script to compile markdown files into HTML, PDF, epub, docx and odt.

## Requirements

* BASH
* Pandoc (http://pandoc.org)
* wkhtmltopdf (http://wkhtmltopdf.org/)

## Usage

The script takes two arguments.
The first is the output directory, into where the compiled files will go.
The second is the draft diretory – the directory containing the markdown files to be assembled into complete documents.

### Example

    $ compile_story.sh /tmp/output ~/path/to/draft

## Other scrips

There are other scripts in this repository as well.

* downdraft.py is a small python application that downloads a directory (typically containing a markdown draft) from dropbox.

* updraft.py uploads compiled files into dropbox.

* cs.sh is a conveniance script for my own setup, that downloads a draft from dropbox, executes the compile\_story-script and uploads all the resulting documents back into dropbox.


