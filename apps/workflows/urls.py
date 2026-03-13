from django.urls import path
from .views import create_workflow, read_workflow

urlpatterns = [
    path('new/', create_workflow, name='new-workflow'),
    path('index/', read_workflow, name='read-workflow')
]