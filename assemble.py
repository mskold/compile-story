#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from zipfile import ZipFile
import sys, fileinput, os, re
from os.path import isfile, isdir, join, basename, dirname
from StringIO import StringIO

try:
    import dropbox
except ImportError:
    sys.stderr.write("Dropbox API not found\n")
    dropbox = False


from config import download_access_token

DROPBOX_TEXT_DIR='/_text/'

METADATAFILE="00-metadata.md"
TITLELEVEL="#"
AUTHORLEVEL="##"
CHAPTERLEVEL="###"
SCENELEVEL="####"
SCENEDIVIDER="· · ·"

def main(sys):
    if len(sys.argv) >= 2:
        # Assume got path to draft
        read_from_disk=True
        if isdir(sys.argv[1]):
            files = [f for f in sorted(os.listdir(sys.argv[1])) if isfile(join(sys.argv[1], f)) and (f.endswith(".md") or f.endswith(".txt"))]
        elif isfile(sys.argv[1]) or len(sys.argv) > 2:
            # Assume got multiple files as input
            files = sorted([basename(sys.argv[i]) for i in range(1,len(sys.argv)) if isfile(sys.argv[i]) and (sys.argv[i].endswith(".md") or sys.argv[i].endswith(".txt"))])
        elif dropbox:
            read_from_disk=False
        else:
            sys.exit("Error: %s is not a directory" % sys.argv[1])
    else:
        sys.exit("Error: No valid arguments supplied")

    if read_from_disk:
        draft_files = load_from_disk(files, dirname(sys.argv[1]))
    else:
        draft_files = load_from_dropbox(sys.argv[1])

    sys.stdout.write(join_files(draft_files, read_from_disk))

def line_replacements(line):
    line = line.replace("***", "%s %s" % (SCENELEVEL, SCENEDIVIDER))
    # Double dashes to en-dashes
    line = line.replace(" -- ", " – ")
    # Replace normal quotes with typographic
    line = line.replace('"','”')
    # Remove trailing whitespace (yes, i think the "double space linebreak" is an abomination in markdown).
    line = line.rstrip(" ")
    return line

def join_files(draft_files, read_from_disk):
    metadata = {}
    manuscript = ""
    chapter_number = 1
    for draft_file in draft_files:
        if draft_file['name'] != METADATAFILE:
            if "storytype" in metadata and metadata['storytype'] == "Novel":
                if "chapterprefix" in metadata:
                    pfx = metadata['chapterprefix']
                    if pfx == "FILENAME":
                        pfx = draft_file['scene_name']
                        manuscript+="\n\n%s %d – %s\n\n" % (CHAPTERLEVEL, chapter_number, pfx)
                    else:
                        manuscript+="\n\n%s %s %d\n\n" % (CHAPTERLEVEL, pfx, chapter_number)
                else:
                    manuscript+="\n\n%s %s\n\n" % (CHAPTERLEVEL, draft_file['scene_name'])
                chapter_number+=1
            elif manuscript != "" and not draft_file['firstline'].startswith("#"):
                manuscript+="\n\n%s %s\n\n" % (SCENELEVEL, SCENEDIVIDER)

        linebuffer = StringIO(draft_file['content'])
        for line in linebuffer:
            if draft_file['name'] == METADATAFILE:
                (key,value) = line.strip().split(": ")
                metadata[key.lower()] = value
            else:
                manuscript+=line_replacements(line)

    if metadata:
        yamlmd="---\n"
        for mdkey, mdval in metadata.items():
            yamlmd+="%s: %s\n" % (mdkey,mdval)
        yamlmd+="---\n\n"
    else:
        yamlmd = ""

    if "title" and "author" in metadata and not read_from_disk:
        titledata="%s %s\n\n%s av %s\n\n\n" % (TITLELEVEL, metadata['title'], AUTHORLEVEL, metadata['author'])
    else:
        titledata=""

    return "%s%s%s" % (yamlmd,titledata,manuscript)

def load_from_disk(files, filepath):
    draft_files = []
    for f in files:
        with open(join(filepath, f), 'r') as draftfile:
            content = draftfile.read()
            firstline = content.split()[0]
            m = re.search('[ |-]{1}(.+?)\.[md|txt]', f)
            if m:
                scene_name = m.group(1)
            else:
                scene_name = f
            draft_files.append({"name": f, "content": content, "firstline": firstline, "scene_name": scene_name})
    return draft_files


def load_from_dropbox(storyname):
    client = dropbox.client.DropboxClient(download_access_token)
    try:
        share_metadata = client.share(join(DROPBOX_TEXT_DIR, '_romaner', storyname, 'draft'), short_url=False)
    except dropbox.rest.ErrorResponse as e:
        sys.stderr.write("%s is apparently not a novel. Trying short story ...\n" % storyname)
        share_metadata = client.share(join(DROPBOX_TEXT_DIR, '_noveller', storyname, 'draft'), short_url=False)

    shareurl = share_metadata['url'].replace('?dl=0','?dl=1')
    sys.stderr.write("Downloading %s from %s\n" % (storyname, shareurl))
    drafturl = urllib2.urlopen(shareurl)

    zipfile = ZipFile(StringIO(drafturl.read()))

    draft_files = []
    for fn in sorted(zipfile.namelist()):
        content = zipfile.open(fn).read()
        if content:
            firstline = content.split()[0]
        else:
            firstline = ""
        m = re.search('[ |-]{1}(.+?)\.[md|txt]', fn)
        if m:
            scene_name = m.group(1)
        else:
            scene_name = fn
        draft_files.append({"name": fn, "content": content, "firstline": firstline, "scene_name": scene_name})

    return draft_files

if __name__ == '__main__':
    main(sys)
