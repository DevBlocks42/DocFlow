from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.http import FileResponse
from django.http import Http404
from apps.utils.paginators import paginate_sort_and_filter
from .forms import CreateDocumentForm
from .models import Document
from django.core.exceptions import ValidationError
import apps.documents.services.document_service as document_service

@login_required
def create_document(request):
    if request.method == 'POST':
        form = CreateDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document_service.create_document(request.user, form)
            messages.success(request, "Document créé avec succès.")
            return redirect('list-documents') 
    else:
        form = CreateDocumentForm()
    return render(request, 'documents/new_doc.html', {'form': form})

@login_required 
def update_document(request):
    document_id = request.GET.get('id')
    user = request.user
    try:
        document = get_object_or_404(Document, id=document_id)
        if not document_service.document_download_allowed(user, document):
            messages.warning(request, "Vous n'avez pas la permission d'accéder à ce document.")
            return redirect('list-documents')
        if not document_service.document_update_allowed(user, document):
            messages.warning(request, "Vous n'avez pas la permission de mettre à jour ce document.")
            return redirect('list-documents')
        if request.method == 'POST':
            form = CreateDocumentForm(request.POST, request.FILES, instance=document)
            if form.is_valid():
                document_service.create_document(user, form)
                messages.success(request, "Document mis à jour.")
            return redirect('list-documents')
        elif request.method == 'GET':
            form = CreateDocumentForm(instance=document)
            return render(request, "documents/new_doc.html", {
                'form': form,
                'document_id': document.id,
                'update': 1
            })
    except Http404:
        messages.warning(request, "Le document n'a pas été trouvé.")
        return redirect('list-documents')


@login_required
def list_documents(request):
    user = request.user
    default_sort_field = "created_at"
    page_number = request.GET.get('page', 1)
    sort_field = request.GET.get('sort_field', default_sort_field)
    sort_order = request.GET.get('sort_order', 'asc')
    filter_field = request.GET.get('filter_field')
    filter = request.GET.get('filter')
    try:
        context = document_service.list_documents(user, page_number, sort_field, sort_order, filter_field, filter)
        context.update({
            'document_status_choices': Document.STATUS_CHOICES
        }) 
    except ValidationError as e:
        messages.warning(request, e.message)
        return redirect('list-documents')
    return render(request, "documents/index.html", context)

@login_required
def download_document(request, document_id):
    user = request.user
    document = get_object_or_404(Document, id=document_id)
    if not document_service.document_download_allowed(user, document):
        messages.warning(request, "Vous n'avez pas la permission de télécharger ce document.")
        return redirect('list-documents')
    return FileResponse(document.file.open('rb'), as_attachment=True)