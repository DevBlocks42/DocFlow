from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateWorkflowForm
from .models import Workflow
from django.contrib import messages
from apps.documents.models import Document
from django.http import Http404
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
import apps.workflows.services.workflows_service as workflow_service
import apps.documents.services.document_service as document_service
from apps.utils.paginators import paginate_sort_and_filter

@login_required
def create_workflow(request): 
    user = request.user
    document_id = request.GET.get("id")
    rejection = int(request.GET.get("reject", -1))
    try:
        document = get_object_or_404(Document, id=document_id)
        if not workflow_service.is_allowed_to_create(user, document):
            messages.warning(request, "Vous n'avez pas la permission d'accéder à ce document.")
            return redirect('list-documents')
    except Http404:
        messages.warning(request, "Le document auquel vous souhaitez accéder n'existe pas.")
        return redirect('list-documents')
    if request.method == "GET":
        form = CreateWorkflowForm()
        return render(request, 'workflows/new_workflow.html', {
            'form': form,
            'rejection': rejection
        })
    elif request.method == "POST":
        form = CreateWorkflowForm(request.POST)
        if form.is_valid():
            workflow, success_message = workflows_service.create_workflow(user, document, form, rejection)
            messages.success(request, success_message)
    return redirect('list-documents')

@login_required 
def read_workflow(request):
    user = request.user 
    document_id = request.GET.get("id")
    default_sort_field = "performed_at"
    page_number = request.GET.get('page', 1)
    sort_field = request.GET.get('sort_field', default_sort_field)
    sort_order = request.GET.get('sort_order', 'asc')
    filter_field = request.GET.get('filter_field')
    filter = request.GET.get('filter')
    try:
        document = get_object_or_404(Document, id=document_id)
        workflows = Workflow.objects.filter(document=document)
        if not document_service.document_download_allowed(user, document):
            messages.warning(request, "Vous n'avez pas la permission de consulter l'historique de ce document.")
            return redirect('list-documents')
        if not workflows.exists():
            messages.warning(request, "Ce document ne possède pas d'historique.")
            return redirect('list-documents')
    except Http404:
        messages.warning(request, "L'historique auquel vous souhaitez accéder n'existe pas.")
        return redirect('list-documents')
    try:
        context = workflow_service.list_workflows(user, workflows, page_number, sort_field, sort_order, filter_field, filter)
        context.update({
            'workflow_status_choices': Workflow.STATUS_CHOICES,
            'document_status_choices': Document.STATUS_CHOICES
        }) 
    except ValidationError as e:
        messages.warning(request, e.message)
        return redirect('list-documents')
    return render(request, "workflows/index.html", context)
    