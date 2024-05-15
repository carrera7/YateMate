from django.urls import path
from . import views

urlpatterns = [
    path('crear_embarcacion/',views.crear_embarcacion,name='crear_embarcacion'),
]