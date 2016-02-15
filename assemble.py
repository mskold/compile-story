#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, fileinput, os, re
from os.path import isfile, isdir, join, basename, dirname
from StringIO import StringIO


METADATAFILE="00-metadata.md"
TITLELEVEL="#"
AUTHORLEVEL="##"
CHAPTERLEVEL="###"
SCENELEVEL="####"
SCENEDIVIDER="· · ·"

def main(sys):
    if len(sys.argv) == 2:
        # Assume got path to draft
        if isdir(sys.argv[1]):
            files = [f for f in sorted(os.listdir(sys.argv[1])) if isfile(join(sys.argv[1], f)) and (f.endswith(".md") or f.endswith(".txt"))]
            add_title_info=False
        else:
            sys.exit("Error: %s is not a directory" % sys.argv[1])
    elif len(sys.argv) > 2:
        # Assume got multiple files as input
        files = sorted([basename(sys.argv[i]) for i in range(1,len(sys.argv)) if isfile(sys.argv[i]) and (sys.argv[i].endswith(".md") or sys.argv[i].endswith(".txt"))])
        add_title_info=False
    else:
        # Asssume reading from appex in iPad
        add_title_info = True
        pass

    draft_files = []
    for f in files:
        with open(join(dirname(sys.argv[1]), f), 'r') as draftfile:
            content = draftfile.read()
            firstline = content.split()[0]
            m = re.search('[ |-]{1}(.+?)\.[md|txt]', f)
            if m:
                scene_name = m.group(1)
            else:
                scene_name = f
            draft_files.append({"name": f, "content": content, "firstline": firstline, "scene_name": scene_name})

    sys.stdout.write(join_files(draft_files, add_title_info))

def line_replacements(line):
    line = line.replace("***", "%s %s" % (SCENELEVEL, SCENEDIVIDER))
    # Double dashes to en-dashes
    line = line.replace(" -- ", " – ")
    # Replace normal quotes with typographic
    line = line.replace('"','”')
    # Remove trailing whitespace (yes, i think the "double space linebreak" is an abomination in markdown).
    line = line.rstrip(" ")
    return line

def join_files(draft_files, add_title_info):
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

    if "title" and "author" in metadata and add_title_info:
        titledata="%s %s\n\n%s av %s\n\n\n" % (TITLELEVEL, metadata['title'], AUTHORLEVEL, metadata['author'])
    else:
        titledata=""

    return "%s%s%s" % (yamlmd,titledata,manuscript)

if __name__ == '__main__':
    main(sys)
