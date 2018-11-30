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
from django.core.exceptions import ValidationError
import smtplib


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


def verify_jwt_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if VerifyJSONWebTokenSerializer().validate(data):
            data = VerifyJSONWebTokenSerializer().validate(data)
            return HttpResponse(
                status=200
            )
        else:
            return HttpResponse(
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
        worker = Worker.objects.all().count()
        if worker > 0:

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
        try:
            data = None
            if request.body:
                data = json.loads(request.body)
            elif request.POST:
                data = request.POST
            if data['permission'] == '2':
                workers = Worker.objects.filter(permission='2')
                if len(workers) > 0:
                    return HttpResponse(
                        json.dumps({'error': 'Already have one admin'}),
                        status=400
                    )
            worker = Worker.objects.create_user(
                username=data['username'],
                password=data['password'],
                cpf=data['cpf'],
                email=data['email'],
                permission=data['permission'])
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("pdf2cash@gmail.com", "Pdf22c@sh*")
            server.sendmail("pdf2cash@gmail.com", data['email'], "Subject: PDF2CASH Senha!! \n\n" + data['password'])
            server.quit()
            worker_dict = worker.__dict__
            worker_dict_real = {}
            worker_dict_real['id'] = worker_dict['id']
            worker_dict_real['username'] = worker_dict['username']
            worker_dict_real['password'] = worker_dict['password']
            worker_dict_real['email'] = worker_dict['email']
            worker_dict_real['cpf'] = worker_dict['cpf']
            worker_dict_real['permission'] = worker_dict['permission']

        except ValidationError:
            return HttpResponse(status=400)

        return HttpResponse(
            json.dumps(worker_dict_real),
            status=201)


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
