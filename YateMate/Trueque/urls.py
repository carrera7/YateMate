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
    path("darDeBajaEmbarcacion/<int:publicacion_id>/",views.darDeBajaEmbarcacion, name="eliminarPublicacionEmbarcacion"),
    path("darDeBajaObjeto/<int:publicacion_id>/",views.darDeBajaObjeto, name="eliminarPublicacionObjeto"),
    path("solicitud_embarcacion/<int:publicacion_id>/",views.solicitud_embarcacion, name="solicitud_embarcacion"),
    path("solicitud_objeto_valioso/<int:publicacion_id>/", views.solicitud_objeto_valioso, name="solicitud_objeto_valioso"),
    path("rechazar_trueque/<int:solicitud_id>/<str:tipo>/", views.rechazar_trueque, name="rechazar_trueque"),
    path("iniciarSolicitudTrueque/<int:solicitudID>/<int:publicacionID>/<str:tipo_objetos>/", views.iniciar_solicitud_de_trueque, name="iniciarSolicitudDeTrueque"),
    path('enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('registrar_Objeto_Valioso/', views.registrar_Objeto_Valioso, name='registrar_Objeto_Valioso'),
    path('registrar_publicacion_boat/', views.registrar_Embarcacion, name='registrar_publicacion_boat'),
    path('finalizar_trueque/<int:publicacion_id>/<str:tipo_obj>/', views.finalizar_trueque, name='finalizar_trueque'),
    path('eliminar_mensaje/<int:mensaje_id>/', views.eliminar_mensaje, name='eliminar_mensaje'),
    path('denunciar/<int:sender_id>/<str:msj>/<int:mensaje_id>/', views.denunciar_usuario, name='denunciar_usuario'),
    path('ver_mensajes_emb/<int:objeto_id>/', views.ver_mensajes_emb, name='ver_mensajes_emb'),
    path('ver_mensajes_obj/<int:objeto_id>/', views.ver_mensajes_obj, name='ver_mensajes_obj'),
    path('ver_informacion_adm/<int:publi_id>/<str:tipo_objeto>/', views.ver_informacion_adm, name='ver_informacion_adm'),
    path('mensajes_denunciados/', views.mensajes_denunciados, name='mensajes_denunciados'),
    path('descartar_denuncia/<int:denuncia_id>/', views.descartar_denuncia, name='descartar_denuncia'),
    path('censurar_mensaje/<int:denuncia_id>/', views.censurar_mensaje, name='censurar_mensaje'),
]