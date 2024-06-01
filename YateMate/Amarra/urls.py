from django.urls import path
from . import views


urlpatterns = [
    path('list_amarra/', views.list_amarra, name="list_amarra"),
    path("VerMisReservas/", views.ver_Reservas, name="misReservas"),
    path("PublicarAlquilerTemporal/", views.publicar_Alquiler, name="publicarAlquiler"),
]


