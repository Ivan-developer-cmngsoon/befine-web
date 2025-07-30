from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

app_name = 'clientes'

urlpatterns = [
    # Autenticación y gestión de cuenta
    path('login/', auth_views.LoginView.as_view(template_name='clientes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('registro/', views.registro_cliente, name='registro'),
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    path('completar-perfil/', views.completar_perfil, name='completar_perfil'),

    # Recuperación de contraseña (flujo completo)
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='clientes/password_reset.html',
        email_template_name='clientes/password_reset_email.html',
        success_url=reverse_lazy('clientes:password_reset_done'),
        extra_context={
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
        }
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='clientes/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='clientes/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='clientes/password_reset_complete.html'
    ), name='password_reset_complete'),
]
