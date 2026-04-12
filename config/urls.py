"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from refugees.views import RefugeesListView, RefugeesCreateView, RefugeesUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registros/', RefugeesListView.as_view(), name="registros"),
    path('registrar/', RefugeesCreateView.as_view(), name="create_refugees"),
    path('atualizar_registro/<int:pk>', RefugeesUpdateView.as_view(), name="update_refugees"),
]
