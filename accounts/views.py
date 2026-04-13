from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login

def register(request):
    if request.method == 'GET':
        return render(request, 'pagina_register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password or not username:
            return HttpResponse("preencher todos os campos")
        
        if User.objects.filter(email = email).exists():
            return HttpResponse("E-mail em uso, por favor tente usar outro E-mail")
        
        user = User.objects.create_user(username=username, email = email, password = password)
        
        return HttpResponse(f"Usuário {username} criado com sucesso!")

def login(request):
    if request.method == 'GET':
        return render(request, 'pagina_login.html')
    else:
       email = request.POST.get('email')
       password = request.POST.get('password')
       
       user = authenticate(request, email=email, password=password)
       
    if user is not None:
        auth_login(request, user)

        if user.is_superuser:
            return redirect('registros')
        else:
            return redirect('base')
    else:
        return HttpResponse("Credenciais inválidas")