from django.urls import path
from .views import list_tela, list_video, NovaTela, EditTela, EditVideo, DeleteTela, NovoVideo

urlpatterns = [
    path('', list_tela, name="list_tela"),
    path('list_video', list_video, name="list_video"),
    path('inserir', NovaTela.as_view(), name="inserir_tela"),
    path('inserir_video', NovoVideo.as_view(), name="inserir_video"),
    path('editar/<int:tela>/', EditTela.as_view(), name="editar-tela"),
    path('editar_video/<int:tela>/', EditVideo.as_view(), name="editar-video"),
    path('delet-tela', DeleteTela.as_view(), name='delete-tela')

]