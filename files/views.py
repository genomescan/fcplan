import json
import os
from django.http import HttpResponse
from django.http import JsonResponse
import jsonschema
import subprocess as sp
from datetime import datetime
import shutil
import signal
import string
from time import sleep
import requests
from pathlib import Path


def csrf_failure(request, reason=""):
    return HttpResponse('CSRF error. Exiting.')


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def nowstr():
    return str(unix_time_millis(datetime.now()))


def index(request):
    return HttpResponse("TEST<img src='/static/images/django.png'>")


def exec_background(info):
    nowstrt = nowstr()
    with open('/home/sbsuser/apis/message-' + nowstrt, 'w') as message_file:
        message_file.write(json.dumps(info))

    prcs = sp.Popen(['python3',
                     '/home/sbsuser/apis/files/execbg.py',
                     nowstrt],
                    stdout=sp.DEVNULL,
                    stderr=sp.DEVNULL,
                    close_fds=True)
    return JsonResponse({'parent_pid': prcs.pid,
                         'job_id': info['job_id']})


def savechange(request):
    f = open('testfile', 'w')
    f.write(request.POST)


def put_file(request):
    if request.user.is_authenticated:
        info = json.loads(request.POST['json'])
        if os.path.isdir(info['location']):
            with open(info['location']+'/'+info['filename'], 'w') as outfile:
                outfile.write(request.FILES['name'].read().decode('utf-8'))
            if os.path.isfile(os.path.join(info['location'], info['filename'])):
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False,
                                     'reason': 'File not created: ' + info['filename']})
        else:
            return JsonResponse({'success': False,
                                 'reason': 'Folder does not exist'})

    else:
        return JsonResponse({'success': False,
                             'reason': 'Could not login on analysis server to put file'})


def test(request):
    if request.user.is_authenticated:
        response = repr(request)
        if len(request.FILES) > 0:
            data = request.FILES['name'].read()
            data = data.decode('utf-8')
            decoded = json.loads(data)
            path = '/media/easystore/Runs/testfolder'
            if not os.path.exists(path):
                os.mkdir(path)
            with open(path+'/samples.json', 'w') as file:
                file.write(data);
            response += pprint.pformat(decoded['samples'][request.POST['sample']], indent=4)
        return HttpResponse(response+"\n")
    else:
        return HttpResponse('NOT LOGGED IN')
