from django.shortcuts import render, redirect
from .models import User
from .choices import Role
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages


def is_admin_user(user):
    return user.is_authenticated and user.is_superuser and user.role == Role.Admin


@login_required(login_url='login')
@user_passes_test(is_admin_user, login_url='login')
def register(request):
    if request.method == 'GET':
        return render(request, 'pagina_register.html')

    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    if not email or not password or not username:
        messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
        return redirect('register')

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "O formato do e-mail inserido é inválido.")
        return redirect('register')

    if User.objects.filter(email=email).exists():
        messages.error(request, "Este e-mail já está em uso. Por favor, utilize outro.")
        return redirect('register')

    try:
        validate_password(password)
    except ValidationError as e:
        for error in e.messages:
            messages.error(request, error)
        return redirect('register')

    User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=Role.Admin,
    )
    messages.success(request, f"Usuário {username} criado com sucesso!")
    return redirect('login')

def login(request):
    if request.method == 'GET':
        return render(request, 'pagina_login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
       
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Bem-vindo de volta, {user.username}!")
            if user.is_superuser:
                return redirect('registros')
            else:
                return redirect('base')
        else:
            messages.error(request, "E-mail ou senha incorretos. Tente novamente.")
            return redirect('login')
        
def user_logout(request):
    logout(request)
    messages.info(request, "Você foi desconectado com segurança.")
    return redirect('home')