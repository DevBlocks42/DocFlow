from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CustomAuthenticationForm
from .forms import UserUpdateForm
from .forms import EditPasswordForm
from apps.documents.services.document_service import get_documents_by_statuses
from apps.documents.models import Document


class UserLoginView(LoginView):
    template_name='users/login.html'
    authentication_form=CustomAuthenticationForm
    redirect_authenticated_user = True

@login_required
def dashboard(request):
    user = request.user 
    documents = get_documents_by_statuses(user)
    profile_form = UserUpdateForm(instance=user)
    password_form = EditPasswordForm(user=user)
    if request.method == 'POST':
        if 'profile-submit' in request.POST:
            profile_form = UserUpdateForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                profile_form.save(commit=True)
                messages.success(request, "Profil mis à jour avec succès.")
                return redirect('dashboard')
        elif 'password-submit' in request.POST:
            password_form = EditPasswordForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Mot de passe changé avec succès.")
                return redirect('dashboard')
    context = {
        "user": user,
        "role": user.role,
        "profile_form": profile_form,
        "password_form": password_form,
        "documents": documents
    }
    return render(request, "users/dashboard.html", context)
