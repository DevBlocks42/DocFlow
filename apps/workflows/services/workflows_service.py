from django.db import transaction
from django.utils import timezone
from ..models import Workflow
from apps.documents.models import Document
from apps.utils.paginators import paginate_sort_and_filter

def is_allowed_to_create(user, document):
    if user.role == 'employe':
        return document.status == Document.STATUS_DRAFT and document.created_by == user 
    elif user.role == 'manager':
        return document.status == Document.STATUS_PENDNG and document.assigned_to == user 
    return False

def create_workflow(user, document, form, rejection=0):
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
    workflow.performed_by = user
    workflow.performed_at = timezone.now()
    with transaction.atomic():
        workflow.save()
        workflow.document.save()
    return workflow, success_message

def list_workflows(user, objects, page_number, sort_field, sort_order, filter_field, filter):
    allowed_fields = ["document__title", "action", "document.status", "performed_by", "comment", "performed_at"]
    context = paginate_sort_and_filter(page_number, sort_field, sort_order, filter_field, filter, objects, "performed_at", allowed_fields)
    context.update({
        'user': user,
        'document_id': objects[0].document.id
    })
    return context