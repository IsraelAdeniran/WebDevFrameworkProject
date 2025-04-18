from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Manager, Assignment, Employee, Trainer, TrainingModule
from .forms import TrainingModuleForm, AssignmentForm

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
    # Get the manager object for this user
    manager = Manager.objects.get(user=request.user)
    department = manager.department

    # Get all assignments for employees in this manager's department
    assignments = Assignment.objects.filter(employee__department=department)

    context = {
        'assignments': assignments,
        'department': department,
    }
    return render(request, 'core/manager_dashboard.html', context)

@login_required
def trainer_dashboard(request):
    trainer = Trainer.objects.get(user=request.user)
    modules = TrainingModule.objects.filter(created_by=trainer)

    context = {
        'modules': modules,
    }
    return render(request, 'core/trainer_dashboard.html', context)

@login_required
def employee_dashboard(request):
    employee = Employee.objects.get(user=request.user)
    assignments = Assignment.objects.filter(employee=employee)
    department = employee.department

    context = {
        'assignments': assignments,
        'department': department,
    }
    return render(request, 'core/employee_dashboard.html', context)

@login_required
def create_training_module(request):
    trainer = Trainer.objects.get(user=request.user)

    if request.method == 'POST':
        form = TrainingModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.created_by = trainer
            module.save()
            return redirect('trainer_dashboard')
    else:
        form = TrainingModuleForm()

    return render(request, 'core/create_training_module.html', {'form': form})

@login_required
def assign_training(request):
    manager = Manager.objects.get(user=request.user)
    department = manager.department

    # Limit employee and module choices
    form = AssignmentForm(request.POST or None)
    form.fields['employee'].queryset = Employee.objects.filter(department=department)
    form.fields['module'].queryset = TrainingModule.objects.all()

    if request.method == 'POST' and form.is_valid():
        assignment = form.save(commit=False)
        assignment.assigned_by = manager
        assignment.status = 'Not Started'
        assignment.save()
        return redirect('manager_dashboard')

    return render(request, 'core/assign_training.html', {'form': form})