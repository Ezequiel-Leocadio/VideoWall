from django.contrib import admin
from django.urls import path
from .views import list_produtos, list_tabela, list_tabela2, inserir_produtos, NewsCreateView, produto_upload, editar_produtos, editar

urlpatterns = [
    path('', list_produtos, name="list_produtos"),
    path('inserir', produto_upload, name="produto_upload"),
    path('editar/<int:id>/', editar_produtos, name="editar_produtos"),
    path('editar', editar, name="editar"),
    path('tabela', list_tabela, name='list_tabela'),
    path('tabela2', list_tabela2, name='list_tabela2'),
    path('create', NewsCreateView, name='news-create'),

]