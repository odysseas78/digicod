from django.urls import path
from django.conf import settings
from rest_framework.routers import SimpleRouter
from django.contrib import admin
from django.conf.urls.static import static



urlpatterns = [
   path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)