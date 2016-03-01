#coding: utf-8
import sys,re, os, collections
from os.path import abspath, isfile, isdir, join, basename, dirname

chapter_index = 0
scene_divider = "#### · · ·"

def parse_metadata(mdcontent):
	metadata = {}
	if mdcontent:
		for mdline in mdcontent.split("\n"):
			if ": " in mdline:
				(key, value) = mdline.split(": ")
				metadata[key] = value
	return metadata

def _join_manuscript(data, metadata, chapter_names):
	global chapter_index
	manuscript = ''
	first_scene = True
	for key, content in data.items():
		if key.startswith("PART:"):
			# Append all data in part
			manuscript += '\n\n## %s\n\n' % key.split('-')[1]
			manuscript += _join_novel(content, metadata, chapter_names)
		else:
			if content.startswith('#'):
				manuscript += '\n\n'
			elif metadata.get('storytype','').lower() == 'Novel'.lower():
				manuscript+=chapter_names[chapter_index]
				chapter_index += 1
			elif not first_scene:
				manuscript+='\n\n%s\n\n' % scene_divider
			manuscript+=content
			first_scene = False
	return manuscript


def _join_files(draft_data, with_yaml):
	metadata = parse_metadata(draft_data.get('00-metadata.md'))
	if '00-metadata.md' in draft_data:
		del draft_data['00-metadata.md']

	chapters = []

	# Join all scenes/chapters
	if metadata.get('storytype','').lower() == 'Novel'.lower():
		if draft_data.pop('parts',False):
			# Count chapters
			numchaps = 0
			for key, possible_part in draft_data.items():
				if key.startswith("PART:"):
					numchaps += len(draft_data[key])
				else:
					numchaps += 1
			chapters = ["\n\n### %s %d\n\n" % (metadata.get("chapterprefix", ""), n) for n in range(1,numchaps)]
			global chapter_index
			chapter_index = 0
		else:
			chapters = ["\n\n### %s %d\n\n" % (metadata.get("chapterprefix", ""), n) for n in range(1,len(draft_data)+1)]

	manuscript = _join_manuscript(draft_data, metadata, chapters)

	if with_yaml:
		yaml_section = "---\n"
		for key, value in metadata.items():
			yaml_section += key + ": " + value + "\n"
		yaml_section += "---\n\n"
	else:
		yaml_section = '# %s\n\n## av %s\n\n' % (metadata.get('title','Utan titel'), metadata.get('author','Okänd'))

	manuscript = yaml_section +  manuscript

	if 'revision' in metadata:
		title = '%s_%s' % (metadata.get('title','draft'), metadata.get('revision'))
	else:
		title = metadata.get('title','draft')

	# replace scene breaks with proper breaks
	manuscript = manuscript.replace("***", scene_divider)
	manuscript = manuscript.replace('"', '”')
	manuscript = manuscript.replace(' -- ', ' – ')
	manuscript = re.sub(' +', ' ', manuscript)
	return (title, manuscript)

def list_files(directory):
	draft_data = collections.OrderedDict()
	if isdir(directory):
		for f in sorted(os.listdir(directory)):
			if isfile(join(directory, f)) and f.endswith(".md"):
				with open(join(directory, f), 'r') as draft_file:
					draft_data[basename(f)] = draft_file.read()
			elif isdir(join(directory, f)):
				draft_data['PART:'+basename(f)] = list_files(join(directory, f))
				draft_data['parts'] = True
	return draft_data

def assemble(start_dir, with_yaml = True):
	directory = start_dir
	while basename(directory) != 'draft':
		directory = abspath(join(directory, '..'))
		if directory == '/':
			# If there is no draft directory, work from the specified directory
			directory = start_dir
			break

	draft_files = list_files(directory)
	return _join_files(draft_files, with_yaml)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.exit("Usage: %s <directory>" % sys.argv[0])
	(title, manuscript) = assemble(abspath(sys.argv[1]))
	print manuscript
