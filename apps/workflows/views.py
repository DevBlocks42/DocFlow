from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateWorkflowForm
from django.contrib import messages
from apps.documents.models import Document
from django.http import Http404
from django.utils import timezone

@login_required
def create_workflow(request):
    document_id = request.GET.get("id")
    try:
        document = get_object_or_404(Document, id=document_id)
        if document.status != Document.STATUS_CHOICES[0][0] or document.created_by != request.user:
            messages.warning(request, "Le document que vous souhaitez soumettre n'est pas accessible.")
            return redirect('list-documents')
    except Http404:
        messages.warning(request, "Le document que vous souhaitez soumettre n'existe pas.")
        return redirect('list-documents')
    if request.method == "GET":
        form = CreateWorkflowForm()
        return render(request, 'workflows/new_workflow.html', {
            'form': form
        })
    elif request.method == "POST":
        form = CreateWorkflowForm(request.POST)
        if form.is_valid():
            workflow = form.save(commit=False)
            workflow.document = document
            workflow.document.status = 'pending'
            workflow.performed_by = request.user
            workflow.performed_at = timezone.now()
            workflow.save()
            workflow.document.save()
            messages.success(request, "Le document a bien été envoyé en validation.")
    return redirect('list-documents')