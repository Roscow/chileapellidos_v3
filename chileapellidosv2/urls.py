from django.contrib import admin
from django.urls import path, include
from apellidos import views
from django.conf.urls import handler404, handler500
from apellidos import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apellidos.urls')),
]

handler404 = 'apellidos.views.error_404'
handler500 = 'apellidos.views.error_500'