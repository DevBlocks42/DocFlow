from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateWorkflowForm
from .models import Workflow
from django.contrib import messages
from apps.documents.models import Document
from django.http import Http404
from django.utils import timezone
from django.db import transaction
import apps.workflows.services.workflows_service as workflows_service

@login_required
def create_workflow(request):
    user = request.user
    document_id = request.GET.get("id")
    rejection = int(request.GET.get("reject", -1))
    try:
        document = get_object_or_404(Document, id=document_id)
        if not workflows_service.is_allowed_to_create(user, document):
            messages.warning(request, "Le document que vous souhaitez valider n'est pas accessible.")
            return redirect('list-documents')
    except Http404:
        messages.warning(request, "Le document que vous souhaitez soumettre n'existe pas.")
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