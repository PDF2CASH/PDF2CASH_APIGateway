# -*- coding: utf-8 -*-
from django.views import View
import json
from .models import Api
from django.http import HttpResponse
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


class gateway(View):

    def operation(self, request):
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
        path = request.path_info.split('/')
        if len(path) < 2:
            return HttpResponse('bad request', status=400)
       
        apimodel = Api.objects.filter(name=path[3])
        if apimodel.count() != 1:
            return HttpResponse('bad request', status=400)

        valid, msg = apimodel[0].check_plugin(request)
        if not valid:
            return HttpResponse(msg, status=400)

        res = apimodel[0].send_request(request)
        if res.headers.get('Content-Type', '').lower() == 'application/json':
            data = res.json()
        else:
            data = res.content
        return HttpResponse(data, status=res.status_code)

    def get(self, request):
        return self.operation(request)

    def post(self, request):
        return self.operation(request)

    def put(self, request):
        return self.operation(request)

    def patch(self, request):
        return self.operation(request)

    def delete(self, request):
        return self.operation(request)
