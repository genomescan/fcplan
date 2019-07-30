from django.db.models import CharField
from django.db.models import Q
from django.http import JsonResponse


def get_json_table_uni(request, model_object):
    project = request.GET['project']
    draw = request.GET['draw']
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    search_term = request.GET['search[value]']
    order_dir = request.GET['order[0][dir]']
    order_column = int(request.GET['order[0][column]'])
    headers = [field.name for field in model_object._meta.get_fields()]
    fields = [f for f in model_object._meta.fields if isinstance(f, CharField)]
    queries = [Q(**{f.name + '__icontains': search_term}) for f in fields]
    qs = Q()
    for query in queries:
        qs = qs | query

    direction = ''
    if order_dir != 'asc':
        direction = '-'

    relation = 'projects'
    print (headers)
    data = model_object.objects.order_by(direction + headers[order_column+1])
    
    if project != '0':
        data = data.filter(**{relation+'__in': [project]})
    
    if search_term != '':
        data = data.filter(qs)

    data = data[start:start + length]
    
    files = []
    for doc in data:
        row = {}
        for header in headers:
            if hasattr(doc, header):
                if header == 'id':
                    row['DT_RowId'] = getattr(doc, header)
                elif doc._meta.get_field(header).get_internal_type() != 'ManyToManyField':
                    value = getattr(doc, header)
                    
                    if doc._meta.get_field(header).get_internal_type() == 'DateTimeField':
                        row[header] = value.strftime('%Y-%m-%d %H:%M')
                    else:
                        row[header] = value
        files.append(row)

    if project != '0':
        recordsFiltered = model_object.objects.filter(qs).filter(**{relation+'__in': [project]}).count()
    else:
        recordsFiltered = model_object.objects.filter(qs).count()

    rt = {'draw': draw,
          'recordsTotal': model_object.objects.count(),
          'recordsFiltered': recordsFiltered,
          'data': files,
          }
    return JsonResponse(rt)
