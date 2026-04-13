from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

def register(request):
    if request.method == 'GET':
        return render(request, 'pagina_register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password or not username:
            return HttpResponse("preencher todos os campos")
        
        if User.objects.filter(username = username).exists():
            return HttpResponse("username já registrado")
                        
        user = User.objects.create_user(username=username, email = email, password = password)
        
        
        return HttpResponse(username)

def login(request):
    if request.method == 'GET':
        return render(request, 'pagina_login.html')
    else:
       username = request.POST.get('username')
       email = request.POST
       password = request.POST.get('password')
       
       