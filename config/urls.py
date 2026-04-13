from django.contrib import admin
from django.urls import path, include
from refugees.views import RefugeesListView, RefugeesCreateView, RefugeesUpdateView, RefugeesDeleteView

urlpatterns = [
    path('auth/', include('accounts.urls'))
    path('admin/', admin.site.urls),
    path('registros/', RefugeesListView.as_view(), name="registros"),
    path('registrar/', RefugeesCreateView.as_view(), name="create_refugee"),
    path('atualizar_registro/<int:pk>', RefugeesUpdateView.as_view(), name="update_refugee"),
    path('deletar_registro/<int:pk>', RefugeesDeleteView.as_view(), name="delete_refugee"), 
]
