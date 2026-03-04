from django.urls import path
from .views import create_document

urlpatterns = [
    path('new-doc/', create_document, name='new-doc')
]