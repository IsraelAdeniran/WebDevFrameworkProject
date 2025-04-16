from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect(request):
    role = request.user.role

    if role == 'manager':
        return redirect('manager_dashboard')
    elif role == 'trainer':
        return redirect('trainer_dashboard')
    elif role == 'employee':
        return redirect('employee_dashboard')
    elif role == 'admin':
        return redirect('/admin/')
    else:
        return redirect('login')

@login_required
def manager_dashboard(request):
    return render(request, 'core/manager_dashboard.html')

@login_required
def trainer_dashboard(request):
    return render(request, 'core/trainer_dashboard.html')

@login_required
def employee_dashboard(request):
    return render(request, 'core/employee_dashboard.html')
