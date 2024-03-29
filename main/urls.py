from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

# schema_view = get_schema_view(title='Blog API')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('menu.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include_docs_urls(title='Menu API')),
    # path('schema/', schema_view)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)