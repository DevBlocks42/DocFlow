from django.urls import path
from .views import create_workflow

urlpatterns = [
    path('new/', create_workflow, name='new-workflow')
]