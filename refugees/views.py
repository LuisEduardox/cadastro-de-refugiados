from django.views.generic import ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Refugees
from accounts.models import User
from accounts.choices import Role

# Create your views here.
class HomeTemplateView(TemplateView):
    template_name = 'home.html'

class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_refugee'] = Refugees.objects.filter(user=self.request.user).exists()
        return context

class RefugeesListView(LoginRequiredMixin, ListView):
    model = Refugees
    template_name = 'refugees/registros.html'
    
    def get_queryset(self):
        # Retorna apenas o refugiado do usuário logado
        return Refugees.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_refugee'] = Refugees.objects.filter(user=self.request.user).exists()
        # Passa o refugiado único (se existir)
        try:
            context['refugee'] = Refugees.objects.get(user=self.request.user)
        except Refugees.DoesNotExist:
            context['refugee'] = None
        return context

class RefugeesUpdateView(LoginRequiredMixin, UpdateView):
    model = Refugees
    template_name = 'refugees/update_refugee.html'
    fields = ["name", "address", "age", "religion", "political_affiliation", "profession", "number_of_children", "family_income", "education_level"]
    success_url = reverse_lazy("registros")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_refugee'] = Refugees.objects.filter(user=self.request.user).exists()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class RefugeesDeleteView(LoginRequiredMixin, DeleteView):
    model = Refugees
    template_name = 'refugees/delete_refugee.html'
    success_url = reverse_lazy("registros")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_refugee'] = Refugees.objects.filter(user=self.request.user).exists()
        return context

    def get_queryset(self):
        return Refugees.objects.filter(user=self.request.user)


def create_refugee_register(request):
    if request.user.is_authenticated and Refugees.objects.filter(user=request.user).exists():
        messages.warning(request, "Você já possui um refugiado registrado. Não é possível criar outro.")
        return redirect('registros')

    template = 'refugees/create_refugee.html'

    if request.method == 'GET':
        return render(request, template)

    name = request.POST.get('name', '').strip()
    address = request.POST.get('address', '').strip()
    age = request.POST.get('age', '').strip()
    religion = request.POST.get('religion', '').strip()
    political_affiliation = request.POST.get('political_affiliation', '').strip()
    profession = request.POST.get('profession', '').strip()
    number_of_children = request.POST.get('number_of_children', '').strip()
    family_income = request.POST.get('family_income', '').strip()
    education_level = request.POST.get('education_level', '').strip()

    required_refugee = [name, address, age, number_of_children, education_level]

    if not request.user.is_authenticated:
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not all(required_refugee + [username, email, password]):
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
            return render(request, template, {'post': request.POST})

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "O formato do e-mail é inválido.")
            return render(request, template, {'post': request.POST})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está em uso.")
            return render(request, template, {'post': request.POST})

        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, template, {'post': request.POST})
    else:
        username = None
        if not all(required_refugee):
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
            return render(request, template, {'post': request.POST})

    try:
        age_int = int(age)
        children_int = int(number_of_children)
    except ValueError:
        messages.error(request, "Idade e número de filhos devem ser números válidos.")
        return render(request, template, {'post': request.POST})

    income = family_income if family_income else '0.00'

    try:
        with transaction.atomic():
            if not request.user.is_authenticated:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role=Role.Default_user,
                )
                auth_login(request, user)
            else:
                user = request.user

            Refugees.objects.create(
                user=user,
                name=name,
                address=address,
                age=age_int,
                religion=religion,
                political_affiliation=political_affiliation,
                profession=profession,
                number_of_children=children_int,
                family_income=income,
                education_level=education_level,
            )
    except Exception:
        messages.error(request, "Ocorreu um erro ao salvar o cadastro. Tente novamente.")
        return render(request, template, {'post': request.POST})

    display_name = username or request.user.username
    messages.success(request, f"Bem-vindo(a), {display_name}! Seu cadastro foi criado com sucesso.")
    return redirect('dashboard')
