#coding: utf-8
import workflow, editor, console, clipboard
import re, os, collections
from os.path import isfile, isdir, join, basename, dirname

def parse_metadata(mdcontent):
	metadata = {}
	if mdcontent:
		for mdline in mdcontent.split("\n"):
			if ": " in mdline:
				(key, value) = mdline.split(": ")
				metadata[key] = value
	return metadata


def join_files(draft_data):
	metadata = parse_metadata(draft_data.get('00-metadata.md'))
	if '00-metadata.md' in draft_data:
		del draft_data['00-metadata.md']

	file_delimeter = "\n\n#### · · ·\n\n"

	# Join all scenes/chapters
	if metadata.get('storytype') == "Novel":
		chapters = ["\n\n### %s %d\n\n" % (metadata.get("chapterprefix", ""), n) for n in range(1,len(draft_data)+1)]
		draft_list = draft_data.values()
		manuscript = ""
		for i in range(0,len(draft_data)):
			manuscript+=chapters[i]
			manuscript+=draft_list[i]
		# Set for replace matching later
		file_delimeter = "\n\n### %s [0-9]+\n\n" % metadata.get("chapterprefix", "")
	else:
		manuscript = file_delimeter.join(draft_data.values())

	pattern = '(%s#{3,4} [A-Za-z0-9åäöÅÄÖ .]+)' % file_delimeter
	matched_scene_breaks = re.findall(pattern, manuscript)
	#print "p", pattern
	#print "m", matched_scene_breaks
	if matched_scene_breaks:
		for matched_break in matched_scene_breaks:
			scene_name = matched_break.split("\n")[4]
			pattern = "#{3,4} [A-Za-z0-9åäöÅÄÖ ·.]+\n\n%s\n\n" % scene_name
			manuscript = re.sub(pattern, scene_name+"\n\n", manuscript, 1, re.MULTILINE)

	# replace scene breaks with proper breaks
	manuscript = manuscript.replace("***", "#### · · ·")

	yaml_section = "---\n"
	for key, value in metadata.items():
		yaml_section += key + ": " + value + "\n"
	yaml_section += "---\n"

	manuscript = yaml_section + '\n' + manuscript

	if 'revision' in metadata:
		title = '%s_%s' % (metadata.get('title','draft'), metadata.get('revision'))
	else:
		title = metadata.get('title','draft')

	manuscript = manuscript.replace('"', '”')
	manuscript = manuscript.repalce(' -- ', ' – ')

	return (title, manuscript)

def list_files(directory):
	draft_data = collections.OrderedDict()
	if isdir(directory):
		for f in os.listdir(directory):
			if isfile(join(directory, f)) and f.endswith(".md"):
				with open(join(directory, f), 'r') as draft_file:
					draft_data[basename(f)] = draft_file.read()
	return draft_data

def assemble(directory):
	draft_files = list_files(directory)
	return  join_files(draft_files)
