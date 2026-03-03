from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm
from .forms import UserUpdateForm

class UserLoginView(LoginView):
    template_name='users/login.html'
    authentication_form=CustomAuthenticationForm

@login_required
def dashboard(request):
    user = request.user 
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        try:
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        except ValidationError as e:
            form.add_error('avatar', e)
    else:
        form = UserUpdateForm(instance=user)
    context = {
        "user": user,
        "role": user.role,
        "form": form
    }
    return render(request, "users/dashboard.html", context)
