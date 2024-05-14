from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('login/logout/', views.logout_view, name='logout'),
    path('register/',views.register,name='register'),
    path('enable_accounts/',views.usuarios_inhabilitados,name='enable_accounts'),
    path('habilitar-usuario/<int:usuario_id>/', views.habilitar_usuario, name='habilitar_usuario'),
]