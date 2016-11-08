#!/usr/bin/env python3
# coding: utf-8
# 

import argparse
import sys, re, io, os


def quotes_and_dashes(manuscript):
    manuscript = manuscript.replace('"', u'”')
    manuscript = manuscript.replace("'", u'’')
    manuscript = manuscript.replace(' -- ', u' – ')
    return manuscript


def renumber_chapters(draft):
    manuscript = []
    chapter_index = 1
    for line in draft.splitlines():
        if re.match('### \d+', line):
            m = re.match('### \d+ (.+)', line)
            if m:
                # Preserve extra text after number
                manuscript.append('### %d %s\n' % (chapter_index, m.group(1)))
            else:
                manuscript.append('### %d\n' % chapter_index)
            chapter_index += 1
        else:
            manuscript.append(line)
    return '\n'.join(manuscript)


def remove_yaml(draft):
    manuscript = []
    notyaml = True
    for line in draft.splitlines():
        if line == '---':
            notyaml = not notyaml
        elif notyaml:
            manuscript.append(line)
    return '\n'.join(manuscript)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Handle markdown for manuscript handling.')
    parser.add_argument('manuscript', metavar='<manuscript.md>')
    parser.add_argument('-f', '--reformat', action='store_true', help='Replace quotes and dashes')
    parser.add_argument('-r', '--renumber', action='store_true', help='Renumber the chapters')
    parser.add_argument('-y', '--remove_yaml', action='store_true', help='Remove YAML section')
    parser.add_argument('-t', '--tempdir', metavar='tmpdir', nargs=1, default='/tmp', help='Specify temporary directory, used for backup (defaults to /tmp')
    parser.add_argument('-o', '--output', action='store_true', help='Return manuscript as output.')

    args = parser.parse_args()

    with io.open(args.manuscript, 'r', encoding='utf8') as f:
        markdown = f.read()

    if args.renumber:
        markdown = renumber_chapters(markdown)
        if args.tempdir:
            tmpfilename = os.path.join(args.tempdir, os.path.basename(args.manuscript))
            os.rename(args.manuscript, tmpfilename)
            with open(args.manuscript, 'w') as o:
                o.write(markdown)
        if not args.output:
            print("Chapters renumberered, original saved as %s" % tmpfilename)

    if args.remove_yaml:
        markdown = remove_yaml(markdown)

    if args.reformat:
        markdown = quotes_and_dashes(markdown)

    if args.output:
        print(markdown.encode('utf-8'))

