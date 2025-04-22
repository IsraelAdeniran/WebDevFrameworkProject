from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Manager, Assignment, Employee, Trainer, TrainingModule, Completion, Feedback, FeedbackResponse
from .forms import TrainingModuleForm, AssignmentForm, FeedbackForm, FeedbackResponseForm

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

    # Mark assignments with feedback status
    for assignment in assignments:
        assignment.feedback_given = Feedback.objects.filter(
            user=employee,
            module=assignment.module
        ).exists()

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

    return render(request, 'core/assign_training.html', {'form': form, 'department': department})

@login_required
def complete_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)

    employee = Employee.objects.get(user=request.user)
    if assignment.employee != employee:
        return redirect('employee_dashboard')

    #  Status
    assignment.status = 'Completed'
    assignment.save()

    completion, created = Completion.objects.get_or_create(
        employee=employee,
        module=assignment.module
    )

    if created:
        print("Completion recorded at:", completion.completed_on)

    return redirect('employee_dashboard')

@login_required
def leave_feedback(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    employee = Employee.objects.get(user=request.user)
    department = employee.department

    if assignment.employee != employee or assignment.status != 'Completed':
        return redirect('employee_dashboard')  # not allowed

    # Prevent duplicate feedback
    if Feedback.objects.filter(user=employee, module=assignment.module).exists():
        return redirect('employee_dashboard')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = employee
            feedback.module = assignment.module
            feedback.save()
            return redirect('employee_dashboard')
    else:
        form = FeedbackForm()

    return render(request, 'core/leave_feedback.html', {'form': form, 'module': assignment.module, 'department': department})

@login_required
def respond_to_feedback(request, feedback_id):
    trainer = Trainer.objects.get(user=request.user)
    feedback = Feedback.objects.get(id=feedback_id)

    # Ensure trainer owns the module
    if feedback.module.created_by != trainer:
        return redirect('trainer_dashboard')

    if FeedbackResponse.objects.filter(feedback=feedback).exists():
        return redirect('trainer_dashboard')

    if request.method == 'POST':
        form = FeedbackResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.feedback = feedback
            response.responder = trainer
            response.save()
            return redirect('trainer_dashboard')
    else:
        form = FeedbackResponseForm()

    return render(request, 'core/respond_to_feedback.html', {
        'form': form,
        'feedback': feedback
    })

@login_required
def training_module_page(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    employee = Employee.objects.get(user=request.user)

    # Only allow assigned employee to view this page
    if assignment.employee != employee:
        return redirect('employee_dashboard')

    # Automatically mark as "In Progress" if not already started
    if assignment.status == 'Not Started':
        assignment.status = 'In Progress'
        assignment.save()

    return render(request, 'core/training_module_page.html', {'assignment': assignment})