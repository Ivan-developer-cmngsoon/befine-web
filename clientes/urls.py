from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'clientes'  # <- ✅ Agregado aquí

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='clientes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    path('registro/', views.registro_cliente, name='registro'),
    path('completar-perfil/', views.completar_perfil, name='completar_perfil'),
]

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='clientes/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='clientes/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='clientes/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='clientes/password_reset_complete.html'), name='password_reset_complete'),
]
