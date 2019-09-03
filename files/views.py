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
    for lane in range(1, 4):
        data[lane] = {'ID': f"id{lane}", 'samples': ['sample1', 'sample2', 'sample3','sample1', 'sample2', 'sample3']}
    return JsonResponse(data)


seqdata = {
    'platform': {10: 'Novaseq6000',
                 2: 'Nextseq500'},
    'flowcells': {10: {'S1': {'lanes': 2,
                              'megareads_per_lane': 800},  # +/- 5%
                       'S2': {'lanes': 2,
                              'megareads_per_lane': 2000},  # +/- 5%
                       'S4': {'lanes': 4,
                              'megareads_per_lane': 2500},  # +/- 5%
                       'SP': {'lanes': 2,
                              'megareads_per_lane': 400}},  # +/- 5%
                  2:  {'mid': {'lanes': 1,
                                'megareads_per_lane': 130},  # +/- 5%
                        'high': {'lanes': 1,
                                 'megareads_per_lane': 400}}  # +/- 5%

                  }
            }


def index_allowed_on_lane(barcode, lane):
    i7_indices1 = [barcodes[0] for barcodes in barcode]
    i5_indices1 = [barcodes[1] for barcodes in barcode]
    indices2 = [sample['index_sequences'] for sample in lane]
    indices3 = []
    for indices in indices2:
        for index in indices:
            indices3.append(index)
    i7_indices2 = [barcodes[0] for barcodes in indices3]
    i5_indices2 = [barcodes[1] for barcodes in indices3]
    problem1 = problem2 = False
    for index1 in i7_indices1:
        for index2 in i7_indices2:
            if index1 == index2:
                problem1 = True
    for index1 in i5_indices1:
        for index2 in i5_indices2:
            if index1 == index2:
                problem2 = True
    return not (problem1 and problem2)


def sample_allowed_on_lane(sample, lane):
    if index_allowed_on_lane(sample['index_sequences'], lane) and \
            project_type_allowed_on_lane(sample['project_type'], lane):
        return True
    else:
        return False


def project_type_allowed_on_lane(project_type, lane):
    return True


def get_sequencable_lanes(request, platform, fctype):
    stagedsampleids = StagedSamples.objects.all().order_by('-megareads').values_list('id', flat=True)  # platform=platform
    ids = []
    stagedsamples = []
    for sample in stagedsampleids:
        ids.append(sample)
        stagedsamples.append(getsampleinfo(sample))
    #print(stagedsamples)
    sequencable_lanes = {'lane0': [], 'lane1': [], 'lane2': [], 'lane3': []}
    current_megareads = 0
    max_megareads = seqdata['flowcells'][int(platform)][fctype]['megareads_per_lane']
    max_lanes = seqdata['flowcells'][int(platform)][fctype]['lanes']
    current_lane = 0
    while current_lane < max_lanes:  # current_megareads < max_megareads and
        for stagedsample in stagedsamples:
            if stagedsample['megareads'] < (max_megareads - current_megareads) \
                    and stagedsample['id'] in ids:
                if sample_allowed_on_lane(stagedsample, sequencable_lanes["lane"+str(current_lane)]):
                    sequencable_lanes["lane"+str(current_lane)].append(stagedsample)
                    current_megareads += stagedsample['megareads']
                    ids.remove(stagedsample['id'])
        current_lane += 1
        current_megareads = 0
    return JsonResponse(sequencable_lanes)


def getsampleinfo(id):
    sample1 = StagedSamples.objects.get(id=int(id))
    result = requests.get('http://localhost/modules/samples/actions/get_staged_info.php?id='+str(sample1.sample_id))
    sample2 = json.loads(result.content)
    sample2['id'] = sample1.pk
    sample2['concentration'] = sample1.nmol
    sample2['megareads'] = sample1.megareads
    sample2['collisioncode'] = 'black'
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
