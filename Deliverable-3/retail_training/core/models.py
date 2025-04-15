from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('trainer', 'Trainer'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.OneToOneField('Manager', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# Role - Specific Models
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

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

# Completion Model
class Completion(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    completed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'module')