from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),

    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
]
