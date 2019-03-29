from django.urls import path
from .views import list_tela, NovaTela, EditTela, NovoItemTela, DeleteItemTela, DeleteTela

urlpatterns = [
    path('', list_tela, name="list_tela"),
    path('inserir', NovaTela.as_view(), name="inserir_tela"),
    path('editar/<int:tela>/', EditTela.as_view(), name="editar-tela"),
    path('inserir-item-tela/<int:tela>/', NovoItemTela.as_view(), name="inserir-item-tela"),
    path('delete-item-tela/<int:item>/', DeleteItemTela.as_view(), name="delete-item-tela"),
    path('delet-tela', DeleteTela.as_view(), name='delete-tela')

]