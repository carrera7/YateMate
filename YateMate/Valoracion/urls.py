from django.urls import path
from . import views

urlpatterns = [
    path('valoraciones_list_pendientes/', views.valoraciones_list_pendientes, name='valoraciones_list_pendientes'),
    path('valoraciones_list_realizadas/', views.valoraciones_list_realizadas, name='valoraciones_list_realizadas'),
    path('valoraciones_list_contestadas/', views.valoraciones_list_contestadas, name='valoraciones_list_contestadas'),
    
    path('eliminar-valoracion-trueque/<int:valoracion_id>/', views.eliminar_valoracion_trueque, name='eliminar_valoracion_trueque'),
    path('eliminar-valoracion-amarra/<int:valoracion_id>/', views.eliminar_valoracion_amarra, name='eliminar_valoracion_amarra'),
    path('valorar_trueque/<int:id>/',views.valorar_trueque, name='valorar_trueque'),
    path('valorar_amarra/<int:id>/', views.valorar_amarra, name='valorar_amarra'),
    
    path('mis_valoraciones/',views.mis_valoraciones, name='mis_valoraciones'),
    path('responder_valoracion_trueque/<int:id>/', views.responder_valoracion_trueque, name='responder_valoracion_trueque'),
    path('responder_valoracion_amarra/<int:id>/', views.responder_valoracion_amarra, name='responder_valoracion_amarra'),
    path('modificar_valoracion_trueque/<int:valoracion_id>/', views.modificar_valoracion_trueque, name='modificar_valoracion_trueque'),
    path('modificar_valoracion_amarra/<int:valoracion_id>/', views.modificar_valoracion_amarra, name='modificar_valoracion_amarra'),

    # Otras rutas
]