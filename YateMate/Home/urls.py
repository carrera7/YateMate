from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('login/logout/', views.logout_view, name='logout'),
    path('register/',views.register,name='register'),
    path('enable_accounts/',views.usuarios_inhabilitados,name='enable_accounts'),
    path('habilitar-usuario/<int:usuario_id>/', views.habilitar_usuario, name='habilitar_usuario'),
    path('listado_clientes/',views.listado_clientes, name='listado_clientes'),
    path('moroso_clientes/<int:cliente_id>/',views.moroso_clientes, name='moroso_clientes'),
    path('cancelar_deuda/<int:cliente_id>/',views.cancelar_deuda, name='cancelar_deuda'),
    path('eliminar_usuario/<int:cliente_id>/', views.eliminar_cuenta , name='eliminar_usuario'),
    path('mi_perfil/<int:cliente_id>/',views.mi_perfil, name="perfil"),
    path('eliminar_cuenta/<int:cliente_id>/',views.eliminar_micuenta, name="eliminar_micuenta")
]