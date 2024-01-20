from http import HTTPStatus
from django.http import JsonResponse

from rest_v2 import models


def getAll(request):
    if request.method == 'GET':
        all_data = models.Student.objects.all()
        return JsonResponse([{
            'id': x.id,
            'name': x.name,
            'age': x.age,
            'sex': x.sex
        } for x in all_data], safe=False, status=HTTPStatus.OK)


def getOne(request, *args, **kwargs):
    request_id = kwargs.get('id')
    all_id = models.Student.objects.values('id')
    for i in all_id:
        if str(i['id']) == str(request_id):
            student = models.Student.objects.get(id=request_id)
            return JsonResponse({
                'id': student.id,
                'name': student.name,
                'age': student.age,
                'sex': student.sex
            },
                safe=False,
                status=HTTPStatus.OK)

    return JsonResponse({'message': 'Not found'}, safe=False, status=HTTPStatus.NOT_FOUND)


def create(request, *args, **kwargs):
    ...


def delete(request, *args, **kwargs):
    ...


def update(request, *args, **kwargs):
    ...
