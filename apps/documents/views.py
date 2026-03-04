from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateDocumentForm

@login_required
def create_document(request):
    if request.method == 'POST':
        form = CreateDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.save()
            messages.success(request, "Document créé avec succès.")
            return redirect('dashboard') 
    else:
        form = CreateDocumentForm()
    return render(request, 'documents/new_doc.html', {'form': form})
