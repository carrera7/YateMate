from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.list, name="list"),
    path("list_publication/", views.list_publication, name="list_publication"),
    path("list_publication_boat/", views.list_publication_boat, name="list_publication_boat"),
    path("mis_publicaciones/", views.mis_publicaciones, name="ver_mis_publicaciones"),
    path("mis_solicitudes/", views.solicitudes_trueque, name="ver_mis_solicitudes"),
]