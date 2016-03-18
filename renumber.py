#!/usr/bin/env python
# coding: utf-8

import os, sys, re
from os.path import isfile, dirname, join

directory = dirname(sys.argv[1])
filelist = []

for chapter_file in os.listdir(sys.argv[1]):
    if re.search(r' \(\d\)\.md', chapter_file):
        sys.exit("ERROR! Don't reorder while there are duplicates.")
    if isfile(join(directory, chapter_file)) and chapter_file.endswith('.md') and re.search(r'\d+[ -].+\.md', chapter_file) and chapter_file != '00-metadata.md':
        filelist.append(chapter_file)

n = len(str(len(filelist)))
i = 0
renames = []
for filename in filelist:
    i += 1
    m = re.search(r'^([\d\.]+)([ -].*\.md)', filename)
    if not m:
        sys.exit('Couldn\'t match filenames!')
    new_filename = str(i).zfill(n) + m.group(2)
    if new_filename != filename:
        renames.append((join(directory, filename), join(directory, new_filename)))
        print "%s -> %s" % (filename, new_filename)

# Rename files in reverse order to guarantee not to overwrite anything
renames.reverse()
for job in renames:
    os.rename(job[0], job[1])
