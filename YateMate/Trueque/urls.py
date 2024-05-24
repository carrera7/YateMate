from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.list, name="list"),
    path("list_publication/", views.list_publication, name="list_publication"),
    path("list_publication_boat/", views.list_publication_boat, name="list_publication_boat"),
    path("mis_publicaciones/", views.mis_publicaciones, name="ver_mis_publicaciones"),
    path("solicitudes_trueque_objeto/<int:publicacion_id>/", views.solicitudes_trueque_objeto, name="solicitudes_trueque_objeto"),
    path("solicitudes_trueque_embarcacion/<int:publicacion_id>/", views.solicitudes_trueque_embarcacion, name="solicitudes_trueque_embarcacion"),
    path('saber_mas/<int:id>/<str:tipo_objetos>/', views.saber_mas, name='saber_mas'),
    path("eliminarObjeto/<int:id>/", views.eliminarObjeto, name='eliminar_objeto'),
    path("eliminarEmbarcacion/<int:id>/", views.eliminarEmbarcacion, name='eliminar_embarcacion'),
    path("solisitar_trueque/<int:publicacion_id>/<str:tipo>/",views.solisitar_trueque, name="solisitar_trueque"),
    path("solicitud_embarcacion/<int:publicacion_id>/",views.solicitud_embarcacion, name="solicitud_embarcacion"),
    path("solicitud_objeto_valioso/<int:publicacion_id>/", views.solicitud_objeto_valioso, name="solicitud_objeto_valioso"),
    path("rechazar_trueque/<int:solicitud_id>/<str:tipo>/", views.rechazar_trueque, name="rechazar_trueque"),
    path("iniciarSolicitudTrueque/<int:solicitudID>/<int:publicacionID>/<str:tipo_objetos>/", views.iniciar_solicitud_de_trueque, name="iniciarSolicitudDeTrueque"),
    path('enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),

]