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
    path('trainer/create-module/', views.create_training_module, name='create_training_module'),
    path('manager/assign/', views.assign_training, name='assign_training'),
    path('employee/complete/<int:assignment_id>/', views.complete_assignment, name='complete_assignment'),
    path('employee/feedback/<int:assignment_id>/', views.leave_feedback, name='leave_feedback'),
    path('trainer/respond/<int:feedback_id>/', views.respond_to_feedback, name='respond_to_feedback'),
    path('employee/module/<int:assignment_id>/', views.training_module_page, name='training_module_page'),
]
