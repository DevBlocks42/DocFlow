from django.urls import path
from .views import create_document, list_documents

urlpatterns = [
    path('new/', create_document, name='new-document'),
    path('list/', list_documents, name='list-documents')
]