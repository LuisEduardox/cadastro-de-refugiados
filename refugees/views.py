from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Refugees

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

class RefugeesCreateView(LoginRequiredMixin, CreateView):
    model = Refugees
    template_name = 'refugees/create_refugee.html'
    fields = ["name", "address", "age", "religion", "political_affiliation", "profession", "number_of_children", "family_income", "education_level"]
    success_url = reverse_lazy("registros")
    
    def dispatch(self, request, *args, **kwargs):
        # Verifica se o usuário já tem um refugiado registrado
        if Refugees.objects.filter(user=request.user).exists():
            messages.warning(request, "Você já possui um refugiado registrado. Não é possível criar outro.")
            return HttpResponseRedirect(reverse_lazy('registros'))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # ← Associa o usuário
        return super().form_valid(form)
    
    
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
