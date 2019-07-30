import subprocess as sp
import sys
import shlex
import json
import requests
import os
from time import sleep

message_filename = '/home/sbsuser/apis/message-'+sys.argv[1]

with open(message_filename, 'r') as message_file:
    info = json.loads(message_file.read())

#os.remove(message_filename)

split = shlex.split(info['command'])

try:
    with open(info['stdout_file'], 'w') as logfile:
        prcs = sp.Popen(split, stdout=logfile, stderr=logfile, cwd=info['runfolder'])
except KeyError as name:  # no stdout_file set
    prcs = sp.Popen(split, stdout=sp.DEVNULL, stderr=sp.DEVNULL, cwd=info['runfolder'])

headers = {'Content-Type': 'application/json'}

ret = {'job_id': info['job_id'], 'child_pid': prcs.pid}

try:
    c = 0
    return_url = info['return_url']
    while True:
        r = requests.post(return_url,
                          data=json.dumps(ret),
                          headers=headers,
                          verify='/home/sbsuser/ssl/gscacert.pem')
        c += 1
        if r.status_code == 200 or c > 50:
            break
        sleep(2)

    streams = prcs.communicate()

    return_code = prcs.returncode

    ret = {'job_id': info['job_id'], 'return_code': return_code}

    c = 0
    while True:
        r = requests.post(return_url,
                          data=json.dumps(ret),
                          headers=headers,
                          verify='/home/sbsuser/ssl/gscacert.pem')
        c += 1
        if r.status_code == 200 or c > 50:
            break
        sleep(2)

except KeyError as name:
    pass
