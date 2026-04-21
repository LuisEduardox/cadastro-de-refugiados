from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Refugees

# Create your views here.
class HomeTemplateView(TemplateView):
    template_name = 'home.html'

class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

class RefugeesListView(LoginRequiredMixin, ListView):
    model = Refugees
    template_name = 'refugees/registros.html'

class RefugeesCreateView(LoginRequiredMixin, CreateView):
    model = Refugees
    template_name = 'refugees/create_refugee.html'
    fields = ["name", "address", "age", "religion", "political_affiliation", "profession", "number_of_children", "family_income", "education_level"]
    success_url = reverse_lazy("registros")
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # ← Associa o usuário
        return super().form_valid(form)
    
    
class RefugeesUpdateView(LoginRequiredMixin, UpdateView):
    model = Refugees
    template_name = 'refugees/update_refugee.html'
    fields = ["name", "address", "age", "religion", "political_affiliation", "profession", "number_of_children", "family_income", "education_level"]
    success_url = reverse_lazy("registros")

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class RefugeesDeleteView(LoginRequiredMixin, DeleteView):
    model = Refugees
    template_name = 'refugees/delete_refugee.html'
    success_url = reverse_lazy("registros")

    def get_queryset(self):
        return Refugees.objects.filter(user=self.request.user)
