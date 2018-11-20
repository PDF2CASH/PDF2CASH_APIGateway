from rest_framework import serializers
from .models import (
    Worker
)


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = ('id', 'username', 'email', 'password', 'cpf', 'permission', 'name')
