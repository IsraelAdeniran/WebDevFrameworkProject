from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Admin, Manager, Trainer, Employee, Department, TrainingModule, Assignment, Completion, Feedback, FeedbackResponse

# Custom User Form
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('First name is required.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError('Last name is required.')
        return last_name


# Custom UserAdmin
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'get_full_name', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
    add_form = CustomUserCreationForm

# Custom Manager, Department & Employee Admin
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'department']


class DepartmentAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        if obj:
            return ['name', 'manager']
        return ['name']


admin.site.register(User, UserAdmin)
admin.site.register(Admin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Trainer)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(TrainingModule)
admin.site.register(Assignment)
admin.site.register(Completion)
admin.site.register(Feedback)
admin.site.register(FeedbackResponse)
