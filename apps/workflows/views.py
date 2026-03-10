from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateWorkflowForm
from .models import Workflow
from django.contrib import messages
from apps.documents.models import Document
from django.http import Http404
from django.utils import timezone
from django.db import transaction

@login_required
def create_workflow(request):
    user = request.user
    document_id = request.GET.get("id")
    rejection = int(request.GET.get("reject", -1))
    try:
        document = get_object_or_404(Document, id=document_id)
        if user.role == 'employe':
            if document.status != Document.STATUS_DRAFT or document.created_by != request.user:
                messages.warning(request, "Le document que vous souhaitez soumettre n'est pas accessible.")
                return redirect('list-documents')
        elif user.role == 'manager':
            if document.status != Document.STATUS_PENDING or document.assigned_to != request.user:
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
            workflow = form.save(commit=False)
            if user.role == 'employe':
                workflow_action = Workflow.STATUS_PENDING
                document_status = Document.STATUS_PENDING
                success_message = "Le document a bien été envoyé en validation."
            elif user.role == 'manager':
                if rejection == 1:
                    workflow_action = Workflow.STATUS_ARCHIVED
                    document_status = Document.STATUS_DRAFT
                    success_message = "Le document a bien été archivé."
                else:
                    workflow_action = Workflow.STATUS_VALIDATED
                    document_status = Document.STATUS_VALIDATED
                    success_message = "Le document a bien été approuvé."
            workflow.action = workflow_action
            workflow.document = document
            workflow.document.status = document_status
            workflow.performed_by = request.user
            workflow.performed_at = timezone.now()
            with transaction.atomic():
                workflow.save()
                workflow.document.save()
            messages.success(request, success_message)
    return redirect('list-documents')