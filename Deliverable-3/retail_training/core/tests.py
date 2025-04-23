from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import *
from core.admin import FeedbackAdmin, DepartmentAdmin

User = get_user_model()

class CoreTests(TestCase):
    def setUp(self):
        # Create client and test users
        self.client = Client()
        self.admin_user = User.objects.create_user(username='admin', role='admin', password='password')
        self.manager_user = User.objects.create_user(username='manager', role='manager', password='password')
        self.trainer_user = User.objects.create_user(username='trainer', role='trainer', password='password')
        self.employee_user = User.objects.create_user(username='employee', role='employee', password='password')

        # Create department and role objects
        self.dept = Department.objects.create(name='Sales')
        self.manager = Manager.objects.create(user=self.manager_user, department=self.dept)
        self.employee = Employee.objects.create(user=self.employee_user, department=self.dept)
        self.trainer = Trainer.objects.create(user=self.trainer_user)
        self.admin = Admin.objects.create(user=self.admin_user)

        # Create training module
        self.module = TrainingModule.objects.create(title='Fire Safety', description='...', created_by=self.trainer)

    def test_models_admin_and_strings(self):
        # Create assignment, completion, feedback, and response
        assignment = Assignment.objects.create(employee=self.employee, module=self.module, assigned_by=self.manager, status='Completed')
        completion = Completion.objects.create(employee=self.employee, module=self.module)
        feedback = Feedback.objects.create(user=self.employee, module=self.module, rating=5, comment="Nice")
        response = FeedbackResponse.objects.create(feedback=feedback, responder=self.trainer, response_text="Thanks")

        # Test __str__ methods
        for obj in [self.manager, self.employee, self.trainer, self.admin_user, self.module, assignment, completion, feedback, response]:
            self.assertTrue(str(obj))

        # Test admin short_comment formatting
        fb_admin = FeedbackAdmin(Feedback, None)
        self.assertEqual(fb_admin.short_comment(feedback), "Nice")

        # Test truncating long comments
        module2 = TrainingModule.objects.create(title="Ethics", description="...", created_by=self.trainer)
        fb_long = Feedback.objects.create(user=self.employee, module=module2, rating=4, comment="A" * 100)
        self.assertTrue(fb_admin.short_comment(fb_long).endswith("..."))

        # Test listing employees in department admin
        dept_admin = DepartmentAdmin(Department, None)
        self.assertIn(self.employee.user.get_full_name(), dept_admin.get_employees(self.dept))

    def test_employee_flow(self):
        # Simulate full training flow for an employee
        assign = Assignment.objects.create(employee=self.employee, module=self.module, assigned_by=self.manager, status='Not Started')
        self.client.login(username='employee', password='password')

        # Start training
        self.client.get(reverse('training_module_page', args=[assign.id]))
        assign.refresh_from_db()
        self.assertEqual(assign.status, 'In Progress')

        # Complete training
        self.client.post(reverse('complete_assignment', args=[assign.id]))
        assign.refresh_from_db()
        self.assertEqual(assign.status, 'Completed')

        # Submit feedback
        response = self.client.post(reverse('leave_feedback', args=[assign.id]), {'rating': 4, 'comment': 'Good'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Feedback.objects.filter(user=self.employee, module=self.module).exists())

    def test_trainer_response_and_dashboard(self):
        # Trainer responds to feedback and sees dashboard
        Completion.objects.create(employee=self.employee, module=self.module)
        feedback = Feedback.objects.create(user=self.employee, module=self.module, rating=5, comment="Waiting")
        self.client.login(username='trainer', password='password')
        self.client.post(reverse('respond_to_feedback', args=[feedback.id]), {'response_text': 'Replied'})
        self.assertTrue(FeedbackResponse.objects.filter(feedback=feedback).exists())
        self.assertEqual(self.client.get(reverse('trainer_dashboard')).status_code, 200)

    def test_manager_assign_and_dashboard(self):
        # Manager assigns training and views dashboard
        self.client.login(username='manager', password='password')
        self.client.post(reverse('assign_training'), {'employee': self.employee.id, 'module': self.module.id})
        self.assertTrue(Assignment.objects.filter(employee=self.employee, module=self.module).exists())
        self.assertEqual(self.client.get(reverse('manager_dashboard')).status_code, 200)

    def test_feedback_uniqueness_constraint(self):
        # Prevent duplicate feedback for same user/module
        Feedback.objects.create(user=self.employee, module=self.module, rating=5, comment="Nice")
        with self.assertRaises(Exception):
            Feedback.objects.create(user=self.employee, module=self.module, rating=4, comment="Duplicate")

    def test_assignment_prevent_duplicate_on_completed(self):
        # Prevent reassigning already completed module
        Assignment.objects.create(
            employee=self.employee,
            module=self.module,
            assigned_by=self.manager,
            status='Completed'
        )
        self.client.login(username='manager', password='password')
        response = self.client.post(reverse('assign_training'), {
            'employee': self.employee.id,
            'module': self.module.id
        })
        assignments = Assignment.objects.filter(employee=self.employee, module=self.module)
        self.assertEqual(assignments.count(), 1)  # Only one assignment should exist

    def test_dashboard_redirect_if_not_logged_in(self):
        # Ensure dashboards are protected by login
        for url_name in ['employee_dashboard', 'trainer_dashboard', 'manager_dashboard']:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login/", response.url)

    def test_invalid_feedback_submission(self):
        # Submitting feedback without rating should not save
        assignment = Assignment.objects.create(employee=self.employee, module=self.module, assigned_by=self.manager, status='Completed')
        self.client.login(username='employee', password='password')
        response = self.client.post(reverse('leave_feedback', args=[assignment.id]), {
            'comment': 'Missing rating'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Feedback.objects.filter(comment="Missing rating").exists())