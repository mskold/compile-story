#!/usr/bin/env python


import os, sys, re
from os.path import isfile, dirname, join


if isfile(sys.argv[1]):
    filename = sys.argv[1]
    original_filename = '%s.original' % filename
    chapter_index = 1
    os.rename(filename, original_filename)
    with open(filename, 'w') as renumbered: 
        with open(original_filename, 'r') as original:
            for line in original:
                if re.match('### \d+', line):
                #if line.startswith('### '):
                    m = re.match('### \d+ (.+)', line)
                    if m:
                        # Preserve extra text after number
                        renumbered.write('### %d %s\n' % (chapter_index, m.group(1)))
                    else:
                        renumbered.write('### %d\n' % chapter_index)
                    chapter_index += 1
                else:
                    renumbered.write(line)


