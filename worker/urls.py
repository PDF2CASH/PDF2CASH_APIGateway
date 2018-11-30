from . import views
from django.urls import path


urlpatterns = [
    path(r'worker/', views.WorkerCreateList.as_view()),
    path(r'worker/<int:pk>/', views.WorkerDeleteShowUpdate.as_view()),
]
