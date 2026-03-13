from django.urls import path
from .views import create_document, list_documents, download_document, update_document

urlpatterns = [
    path('new/', create_document, name='new-document'),
    path('update/', update_document, name='update-document'),
    path('list/', list_documents, name='list-documents'),
    path('download/<int:document_id>', download_document, name='download-document')
]