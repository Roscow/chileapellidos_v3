from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detalle_apellido', views.detalle_apellido, name='detalle_apellido'),  
    path('ranking_cantidad_desc/<int:pagina>', views.ranking_cantidad_desc, name='ranking_cantidad_desc'),  
    path('ranking_cantidad_asc/<int:pagina>', views.ranking_cantidad_asc, name='ranking_cantidad_asc'),  
    path('ranking_promedio_edad_desc/<int:pagina>', views.ranking_promedio_edad_desc, name='ranking_promedio_edad_desc'),  
    path('ranking_promedio_edad_asc/<int:pagina>', views.ranking_promedio_edad_asc, name='ranking_promedio_edad_asc'),  
    path('combinar', views.combinar, name='combinar'),  
    path('comparar', views.comparar, name='comparar'),  
    path('ranking_dif_genero_asc/<int:pagina>', views.ranking_dif_genero_asc, name='ranking_dif_genero_asc'),  
    path('ranking_dif_genero_desc/<int:pagina>', views.ranking_dif_genero_desc, name='ranking_dif_genero_desc'),  
]       