# -*- coding: utf-8 -*-
import requests
import json
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import BasicAuthentication


# Create your models here.
class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apikey = models.CharField(max_length=32)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username


class Api(models.Model):
    PLUGIN_CHOICE_LIST = (
        (0, _('Remote auth')),
        (1, _('Basic auth')),
        (2, _('Key auth')),
        (3, _('Server auth'))
    )
    name = models.CharField(max_length=128, unique=True)
    request_path = models.CharField(max_length=255)
    upstream_url = models.CharField(max_length=255)
    plugin = models.IntegerField(choices=PLUGIN_CHOICE_LIST, default=0)
    consumers = models.ManyToManyField(Consumer, blank=True)

    def check_plugin(self, request):
        if self.plugin == 0:
            return True, ''

        elif self.plugin == 1:
            auth = BasicAuthentication()
            try:
                user, password = auth.authenticate(request)
            except Exception:
                return False, 'Authentication credentials were not provided'

            if self.consumers.filter(user=user):
                return True, ''
            else:
                return False, 'permission not allowed'
        elif self.plugin == 2:
            apikey = request.META.get('HTTP_APIKEY')
            consumers = self.consumers.all()
            for consumer in consumers:
                if apikey == consumer.apikey:
                    return True, ''
            return False, 'apikey need'
        elif self.plugin == 3:
            consumer = self.consumers.all()
            if not consumer:
                return False, 'consumer need'
            request.META['HTTP_AUTHORIZATION'] = requests.auth._basic_auth_str(
                consumer[0].user.username,
                consumer[0].apikey
            )
            return True, ''
        else:
            raise NotImplementedError(
                "plugin %d not implemented" % self.plugin
            )

    def send_request(self, request):
        headers = {}
        if self.plugin != 1 and request.META.get('HTTP_AUTHORIZATION'):
            headers['authorization'] = request.META.get('HTTP_AUTHORIZATION')
        # headers['content-type'] = request.content_type

        strip = '/service' + self.request_path
        full_path = request.get_full_path()[len(strip)+4:]
        url = self.upstream_url + full_path
        method = request.method.lower()
        method_map = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'patch': requests.patch,
            'delete': requests.delete
        }

        data = None
        if request.body:
            data = json.loads(request.body)
        elif request.POST:
            data = request.POST

        return method_map[method](
            url,
            headers=headers,
            data=data,
            files=request.FILES
        )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
