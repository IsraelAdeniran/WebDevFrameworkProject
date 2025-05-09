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
    list_display = ['user', 'department']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'department']

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'get_employees']

    def get_fields(self, request, obj=None):
        if obj:
            return ['name', 'manager']
        return ['name']

    def get_employees(self, obj):
        employees = obj.employees.all()
        return ", ".join([e.user.get_full_name() for e in employees])
    get_employees.short_description = "Employees"

# Custom Training Module Admin
class TrainingModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'description']

# Custom Completion Module Admin
class CompletionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'module', 'completed_on']

#Custom Feedback Admin
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'rating', 'created_at', 'short_comment']
    search_fields = ['user__user__first_name', 'user__user__last_name', 'module__title']
    list_filter = ['rating', 'created_at', 'module']

    def short_comment(self, obj):
        return (obj.comment[:50] + '...') if len(obj.comment) > 50 else obj.comment
    short_comment.short_description = "Comment"

admin.site.register(User, UserAdmin)
admin.site.register(Admin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Trainer)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(TrainingModule, TrainingModuleAdmin)
admin.site.register(Assignment)
admin.site.register(Completion,CompletionAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackResponse)
