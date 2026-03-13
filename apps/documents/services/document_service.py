from apps.utils.paginators import paginate_sort_and_filter
from ..models import Document

def create_document(user, form):
    document = form.save(commit=False)
    document.created_by = user
    document.save()
    return document

def list_documents(user, page_number, sort_field, sort_order, filter_field, filter):
    if user.role == "employe":
        documents = Document.objects.filter(created_by=user)
    elif user.role == "manager":
        documents = Document.objects.filter(assigned_to=user, status=Document.STATUS_PENDING)
    elif user.role == "admin":
        documents = Document.objects.all()
    allowed_fields = ["title", "description", "category__name", "assigned_to__username", "created_by__username", "created_at", "status"]
    context = paginate_sort_and_filter(page_number, sort_field, sort_order, filter_field, filter, documents, "created_at", allowed_fields)
    context.update({
        'user': user
    })
    return context

def document_download_allowed(user, document):
    if user.role == 'manager':
        return user == document.assigned_to
    elif user.role == 'employe':
        return user == document.created_by
    elif user.role == 'admin':
        return True 
    return False

def document_update_allowed(user, document):
    if user.role == 'employe':
        return user == document.created_by and document.status == Document.STATUS_DRAFT
    elif user.role == 'admin':
        return True 
    return False