from django.urls import path

from . import views

urlpatterns = [
    path("list_publication/", views.list_publication, name="list_publication"),
]