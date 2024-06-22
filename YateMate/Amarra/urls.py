from django.urls import path
from . import views


urlpatterns = [
    path('list_amarra/', views.list_amarra, name="list_amarra"),
    path('mis_publicaciones_Amarras/', views.mis_publicaciones, name='mis_publicaciones'), 
    path('eliminar_publicacion/<int:id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('modificar_publicacion/<int:id>/', views.modificar_publicacion, name='modificar_publicacion'),
    path('crear_reserva/<int:publicacion_id>/', views.crear_reserva, name='crear_reserva'),
    path('ver_reservas/<int:id>/', views.ver_reservas, name='ver_reservas'),
    path('reservas/', views.reservas, name='reservas'),
    path('reservas/registrar_ingreso/<int:id>/', views.registrar_ingreso, name='registrar_ingreso'),
    path('reservas/registrar_salida/<int:id>/', views.registrar_salida, name='registrar_salida'),
    path("PublicarAlquilerTemporal/", views.publicar_Alquiler, name="publicarAlquiler"),
    path("Ver_mis_reservas/",views.mis_reservas,name="Ver_mis_reservas"),
    path('eliminar_reserva/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
]


