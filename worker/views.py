from .serializers import (
    WorkerSerializer
)
from .models import (
    Worker
)
from django.views import View
import json
from django.http import HttpResponse
from django.http import Http404
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def obtain_jwt_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if JSONWebTokenSerializer().validate(data):
            data = JSONWebTokenSerializer().validate(data)
            return HttpResponse(
                json.dumps({'token': data['token']}),
                status=200
            )
        else:
            return HttpResponse(
                json.dumps({'error': 'authentication error'}),
                status=400
            )
    else:
        return HttpResponse(
            json.dumps({'error': 'just post method is accepted'}),
            status=400
        )


def refresh_jwt_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if RefreshJSONWebTokenSerializer().validate(data):
            data = RefreshJSONWebTokenSerializer().validate(data)
            return HttpResponse(
                json.dumps({'token': data['token']}),
                status=200
            )
        else:
            return HttpResponse(
                json.dumps({'error': 'refresh error'}),
                status=400
            )
    else:
        return HttpResponse(
            json.dumps({'error': 'just post method is accepted'}),
            status=400
        )


class WorkerCreateList(View):

    def get(self, request):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if not VerifyJSONWebTokenSerializer().validate(data):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return HttpResponse(json.dumps(serializer.data))

    def post(self, request):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if not VerifyJSONWebTokenSerializer().validate(data):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        serializer = WorkerSerializer(data=json.loads(request.body))
        if serializer.is_valid():
            data = json.loads(request.body)
            if data['permission'] == '2':
                workers = Worker.objects.filter(permission='2')
                if len(workers) > 0:
                    return HttpResponse(
                        json.dumps({'error': 'Already have one admin'}),
                        status=400
                    )
            serializer.save()
            return HttpResponse(json.dumps(serializer.data), status=201)
        return HttpResponse(json.dumps(serializer.errors), status=400)


def get_object(pk):
    try:
        return Worker.objects.get(pk=pk)
    except Worker.DoesNotExist:
        raise Http404


class WorkerDeleteShowUpdate(View):

    def get(self, request, pk):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if not VerifyJSONWebTokenSerializer().validate(data):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        worker = get_object(pk)
        serializer = WorkerSerializer(worker)
        return HttpResponse(json.dumps(serializer.data))

    def post(self, request, pk):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if not VerifyJSONWebTokenSerializer().validate(data):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        worker = get_object(pk)
        serializer = WorkerSerializer(worker, data=json.loads(request.body))
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json.dumps(serializer.data))
        return HttpResponse(json.dumps(serializer.errors), status=400)

    def delete(self, request, pk):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if not VerifyJSONWebTokenSerializer().validate(data):
            return HttpResponse(
                json.dumps({'error': 'Authorization is required'}),
                status=400
            )
        worker = get_object(pk)
        worker.delete()
        return HttpResponse(status=204)
