import dropbox
import sys
from os import listdir
from os.path import isfile, join

from config import upload_access_token

output_path='/tmp/cs/output'

if len(sys.argv) < 2:
    print "Usage: %s <storyname>" % sys.argv[0]
    exit(1)

storyname = sys.argv[1]

documents = [ f for f in listdir(output_path) if isfile(join(output_path, f)) ]

client = dropbox.client.DropboxClient(upload_access_token)

for doc in documents:
    f = open(join(output_path, doc), 'rb')
    response = client.put_file(join(storyname, doc), f, overwrite=True)
    print 'uploaded', response['path']
    

