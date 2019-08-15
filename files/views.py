import json
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import jsonschema
import subprocess as sp
from datetime import datetime
from .models import StagedSamples
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


def getflowcell(request):
    data = {}
    for lane in range(1,20):
        data[lane] = {'ID': f"id{lane}", 'samples': ['sample1', 'sample2', 'sample3','sample1', 'sample2', 'sample3']}
    return JsonResponse(data)


seqdata = {
    'platform': {10: '',
                 2: 'Nextseq500'},
    'a': 'b'
}


def get_sequencable_lanes(request, platform):
    pass


def getsampleinfo(id):
    sample1 = StagedSamples.objects.get(id=id)
    result = requests.get('http://localhost/modules/samples/actions/get_staged_info.php?id='+str(sample1.sample_id))
    sample2 = json.loads(result.content)
    sample2['concentration'] = sample1.nmol
    sample2['megareads'] = sample1.megareads
    return sample2


def savechange(request):
    f = open('testfile', 'w')
    print(request.POST)
    return HttpResponse('[savechange] werkt')


def stagesample(request):
    stagedsample = StagedSamples(nmol=request.POST['nmol'],
                                 megareads=request.POST['yield'],
                                 sample_id=request.POST['sample_id'])
    stagedsample.save()

    return HttpResponse('[stagesample] werkt')


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
    return render(request, 'test.j2.html')
