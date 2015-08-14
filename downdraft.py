# Include the Dropbox SDK
import dropbox
import urllib2, zipfile
import os, sys, errno
from os.path import join, isdir, basename

from config import download_access_token

TMP_DRAFT_DIRECTORY='/tmp/cs/draft/'
TEXT_DIR='/_text/'

if len(sys.argv) < 2:
    print("Usage: %s <storyname>" % sys.argv[0])
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
    share_metadata = client.share(join(TEXT_DIR, storyname, 'draft'), short_url=False)
except dropbox.rest.ErrorResponse as e:
    print("%s apparently not a novel. Trying short story ..." % storyname)
    share_metadata = client.share(join(TEXT_DIR, '_noveller', storyname, 'draft'), short_url=False)

mkdir_p(TMP_DRAFT_DIRECTORY)

shareurl = share_metadata['url'].replace('?dl=0','?dl=1')
print("Downloading %s" % shareurl)
drafturl = urllib2.urlopen(shareurl)

with open(join(TMP_DRAFT_DIRECTORY, 'draft.zip'), 'wb') as out:
    out.write(drafturl.read())


zfile = zipfile.ZipFile(join(TMP_DRAFT_DIRECTORY, 'draft.zip'))
zfile.extractall(TMP_DRAFT_DIRECTORY)

os.remove(join(TMP_DRAFT_DIRECTORY, 'draft.zip'))
