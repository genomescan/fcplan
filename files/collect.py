import sys
import json
import requests
import os
from pathlib import Path
from time import sleep

message_filename = '/home/sbsuser/apis/message-'+sys.argv[1]

with open(message_filename, 'r') as message_file:
    info = json.loads(message_file.read())

#os.remove(message_filename)

number_of_files = 0
for location in info['locations']:
    if not Path(location['target']).is_dir():
        os.mkdir(location['target'])
    for file in info['files']:
        if Path(location['source']+"/"+file).is_file():
            os.rename(location['source']+"/"+file, location['target']+"/"+file)
uniq_locations = set([])
for location in info['locations']:
    uniq_locations.add(location['target'])
for location in uniq_locations:
    number_of_files += len([name for name in os.listdir(location)
                            if name.endswith('.fastq.gz') and
                            os.path.isfile(os.path.join(location, name))])

ret = {'job_id': info['job_id'],
       'number_of_files': number_of_files,
       'files_in_filelist': len(info['files']),
       'locations': info['locations']}

headers = {'Content-Type': 'application/json'}

c = 0
while True:
    r = requests.post(info['return_url'],
                      data=json.dumps(ret),
                      headers=headers,
                      verify='/home/sbsuser/ssl/gscacert.pem')
    c += 1
    if r.status_code == 200 or c > 50:
        break
    sleep(2)
