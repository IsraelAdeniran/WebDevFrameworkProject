from django import forms
from .models import TrainingModule, Assignment

class TrainingModuleForm(forms.ModelForm):
    class Meta:
        model = TrainingModule
        fields = ['title', 'description']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['employee', 'module']