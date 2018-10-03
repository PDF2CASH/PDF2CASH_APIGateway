from rest_framework import viewsets
from .serializers import (
    WorkerSerializer
)
from .models import (
    Worker
)


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
