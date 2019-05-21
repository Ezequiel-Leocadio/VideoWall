
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls'),name='home'),
    path('produto', include('produtos.urls')),
    path('tv', include('tvs.urls')),
    path('tela', include('telas.urls')),
    path('oferta', include('ofertas.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

