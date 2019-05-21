from django.urls import path
from .views import list_oferta, NovaOferta,  EditOferta, DeleteOferta, lista_produtos_auto_ajax

urlpatterns = [
    path('', list_oferta, name="list_oferta"),
    path('inserir/', NovaOferta.as_view(), name="inserir_oferta"),
    path('editar-oferta/<int:oferta>/', EditOferta.as_view(), name="editar-oferta"),
    path('delet-oferta', DeleteOferta.as_view(), name='delete-oferta'),
    path('con_ajax_post',  lista_produtos_auto_ajax, name='con_ajax_post')
]