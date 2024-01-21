# import json
# from http import HTTPStatus
# from django.http import JsonResponse, HttpResponse
# from rest_v2 import models
#
#
# def getAll(request):
#     if request.method == 'GET':
#         all_data = models.Student.objects.all()
#         return JsonResponse([{
#             'id': x.id,
#             'name': x.name,
#             'age': x.age,
#             'sex': x.sex
#         } for x in all_data], safe=False, status=HTTPStatus.OK)
#
#
# def getOne(request, *args, **kwargs):
#     request_id = kwargs.get('id')
#     all_id = models.Student.objects.values('id')
#     for i in all_id:
#         if str(i['id']) == str(request_id):
#             student = models.Student.objects.get(id=request_id)
#             return JsonResponse({
#                 'id': student.id,
#                 'name': student.name,
#                 'age': student.age,
#                 'sex': student.sex
#             },
#                 safe=False,
#                 status=HTTPStatus.OK)
#
#     return JsonResponse({'message': 'Not found'}, safe=False, status=HTTPStatus.NOT_FOUND)
#
#
# def create(request):
#     data = request.body.decode('utf-8')
#     data = json.loads(data)
#
#     if data:
#         name = data['name']
#         age = data['age']
#         sex = data['sex']
#         response_data = models.Student.objects.create(name=name, age=age, sex=sex)
#         return JsonResponse({
#             'id': response_data.id,
#             'name': response_data.name,
#             'age': response_data.age,
#             'sex': response_data.sex
#         }, safe=False, status=HTTPStatus.CREATED)
#
#     return JsonResponse({'message': 'Data is not valid'}, safe=False, status=404)
#
#
# def delete(request, *args, **kwargs):
#     ...
#
#
# def update(request, *args, **kwargs):
#     ...


# views.py
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_v2 import models


@method_decorator(csrf_exempt, name='dispatch')
class StudentListView(View):
    def get(self, request, *args, **kwargs):
        objects = models.Student.objects.all()
        serialized_data = [{'id': obj.id, 'name': obj.name, 'age': obj.age, 'sex': obj.sex} for obj in objects]
        return JsonResponse(serialized_data, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        obj = models.Student.objects.create(
            name=data.get('name', ''),
            age=data.get('age', ''),
            sex=data.get('sex', ''),
        )

        serialized_data = {'id': obj.id, 'name': obj.name, 'age': obj.age, 'sex': obj.sex}
        return JsonResponse(serialized_data, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class StudentDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(models.Student, pk=kwargs['pk'])
        serialized_data = {'id': obj.id, 'name': obj.name, 'age': obj.age, 'sex': obj.sex}
        return JsonResponse(serialized_data)

    def put(self, request, *args, **kwargs):
        obj = get_object_or_404(models.Student, pk=kwargs['pk'])
        data = json.loads(request.body.decode('utf-8'))

        obj.name = data.get('name', obj.name)
        obj.age = data.get('age', obj.age)
        obj.sex = data.get('sex', obj.sex)
        obj.save()

        serialized_data = {'id': obj.id, 'name': obj.name, 'age': obj.age, 'sex': obj.sex}
        return JsonResponse(serialized_data)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(models.Student, pk=kwargs['pk'])
        print(len(kwargs))
        obj.delete()
        return JsonResponse({'message': 'Object deleted successfully'}, status=204)
