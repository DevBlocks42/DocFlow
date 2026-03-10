from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateDocumentForm
from .models import Document
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from apps.utils.paginators import paginate_sort_and_filter

@login_required
def create_document(request):
    if request.method == 'POST':
        form = CreateDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.save()
            messages.success(request, "Document créé avec succès.")
            return redirect('list-documents') 
    else:
        form = CreateDocumentForm()
    return render(request, 'documents/new_doc.html', {'form': form})

@login_required
def list_documents(request):
    documents = []
    user = request.user
    if user.role == "employe":
        documents = Document.objects.filter(created_by=user, status=Document.STATUS_CHOICES[0][0])
    elif user.role == "manager":
        documents = Document.objects.filter(assigned_to=user, status=Document.STATUS_CHOICES[1][0])
    elif user.role == "admin":
        documents = Document.objects.all()
    allowed_fields = ["title", "description", "category__name", "assigned_to__username", "created_by__username", "created_at", "status"]
    context = paginate_sort_and_filter(request, documents, "created_at", allowed_fields)
    context.update({
        'user': user
    })
    return render(request, "documents/index.html", context)

