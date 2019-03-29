from django.urls import path
from .views import list_tv, list_tabela

urlpatterns = [
    path('', list_tv, name="list_tv"),
    path('tabela',list_tabela, name="list_tabela"),
]