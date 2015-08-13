# Include the Dropbox SDK
import dropbox
import os, sys, errno
from os.path import join, isdir, basename

from config import download_access_token

TMP_DRAFT_DIRECTORY='/tmp/cs/draft'
NOVEL_DRAFT_DIR='/_text/'
SHORT_STORY_DRAFT_DIR='/_text/_noveller'

if len(sys.argv) < 2:
    print "Usage: %s <storyname>" % sys.argv[0]
    exit(1)

storyname = sys.argv[1]

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and isdir(path):
            pass
        else: raise

client = dropbox.client.DropboxClient(download_access_token)
try:
    folder_metadata = client.metadata(join(NOVEL_DRAFT_DIR, storyname, 'draft'))
except dropbox.rest.ErrorResponse as e:
    print "%s apparently not a novel. Trying short story ..." % storyname
    folder_metadata = client.metadata(join(SHORT_STORY_DRAFT_DIR, storyname, 'draft'))

mkdir_p(TMP_DRAFT_DIRECTORY)

for scene in folder_metadata['contents']:
    if scene['is_dir'] == False:
        filename = basename(scene['path'])
        outfile = join(TMP_DRAFT_DIRECTORY, filename)
        out = open(outfile, 'wb')
        with client.get_file(scene['path']) as f:
            print 'downloading', scene['path']
            out.write(f.read())
