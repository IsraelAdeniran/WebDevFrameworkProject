from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

# User Model
class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')  # Automatically sets role
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('trainer', 'Trainer'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name'] # Prompt for Name & Email

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.OneToOneField('Manager', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_department')

    def __str__(self):
        return self.name

# Role - Specific Models
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.get_full_name()} (Admin)"

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='managers')

    def __str__(self):
        return f"{self.user.get_full_name()} (Manager)"

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.get_full_name()} (Trainer)"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    def __str__(self):
        return f"{self.user.get_full_name()} (Employee)"

# Training - Module Model
class TrainingModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

# Assignment Model
class Assignment(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(Manager, on_delete=models.CASCADE)
    assigned_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')

    def __str__(self):
        return f"{self.employee.user.get_full_name()} → {self.module.title} [{self.status}]"

# Completion Model
class Completion(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    completed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'module')

    def __str__(self):
        return f"{self.employee.user.get_full_name()} completed {self.module.title}"

# Feedback Model
class Feedback(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'module')

    def __str__(self):
        return f"Feedback by {self.user.user.get_full_name()} on {self.module.title}"

# Feedback - Response Model
class FeedbackResponse(models.Model):
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE)
    responder = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    response_text = models.TextField()
    responded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.responder.user.get_full_name()} to feedback #{self.feedback.id}"