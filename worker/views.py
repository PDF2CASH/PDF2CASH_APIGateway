from rest_framework import viewsets
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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


class WorkerCreateList(View):

    def get(self, request):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if VerifyJSONWebTokenSerializer().validate(data) == False:
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return HttpResponse(json.dumps(serializer.data))

    def post(self, request):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if VerifyJSONWebTokenSerializer().validate(data) == False:
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        serializer = WorkerSerializer(data=request.POST)
        if serializer.is_valid():
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
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if VerifyJSONWebTokenSerializer().validate(data) == False:
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        worker = get_object(pk)
        serializer = WorkerSerializer(worker)
        return HttpResponse(json.dumps(serializer.data))

    def post(self, request, pk):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if VerifyJSONWebTokenSerializer().validate(data) == False:
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        worker = get_object(pk)
        serializer = WorkerSerializer(worker, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json.dumps(serializer.data))
        return HttpResponse(json.dumps(serializer.errors), status=400)

    def delete(self, request, pk):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        token = request.META['HTTP_AUTHORIZATION'].replace('JWT ', '')
        data = {'token': token}
        if VerifyJSONWebTokenSerializer().validate(data) == False:
            return HttpResponse(json.dumps({'error': 'Authorization is required'}), status=400)
        worker = get_object(pk)
        worker.delete()
        return HttpResponse(status=204)
