from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core import mail

from models import Team;
from models import TeamMember;
from models import Task; 

#Matteo's code - assisted by MS manuals on Django testing, CGPT, and Copilot.

class AboutTests(TestCase):

    # Test to check if the About page renders correctly
    def test_about_page_status_code(self):
        response = self.client.get(reverse('about'))  # Replace with your URL name if different
        self.assertEqual(response.status_code, 200)

    # Check header
    def test_about_page_content(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, '<h1>About</h1>')
        self.assertContains(response, 'Lorem ipsum dolor sit amet')

    # Test for correct members
    def test_about_page_team_member_count(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'Jake')
        self.assertContains(response, 'John')
        self.assertContains(response, 'Matteo')
        self.assertContains(response, 'Syed')
        self.assertContains(response, 'Yumna')

    # Test for a logged-out user showing the login button
    def test_logged_out_user_sees_login_button(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'Login')

    # Test for a logged-in user seeing the logout button
    def test_logged_in_user_sees_logout_button(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('about'))
        self.assertContains(response, 'Logout')
        self.assertContains(response, 'testuser@example.com') 

    # Test for correct team member image URLs 
    def test_team_member_images(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'https://lh3.googleusercontent.com/d/1dV6fxNiAayJDuKjPDdsMW83DS8ROet1x=s220?authuser=0')  # Example URL
        self.assertContains(response, 'https://lh3.googleusercontent.com/d/1H2ttzpLVDMQ_3rpXGHQyWiQALZI0a5RF?authuser=0')

    # Test CSS
    def test_about_page_css(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'background-color: #e0e0e0')
        self.assertContains(response, 'padding: 20px')

class CreateTeamTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_create_team_page_accessible(self):
        response = self.client.get(reverse('createTeam'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Team Name')  
        self.assertContains(response, 'Description')  

    def test_csrf_token_in_form(self):
        response = self.client.get(reverse('createTeam'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_create_team_form_invalid(self):
        response = self.client.post(reverse('createTeam'), {
            'name': '',  
            'description': '',  
        })

        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'description', 'This field is required.')

        def test_create_team_form_valid(self):
            response = self.client.post(reverse('createTeam'), {
            'name': 'Test Team',
            'description': 'A team for testing purposes',
        })

        self.assertEqual(Team.objects.count(), 1)
        team = Team.objects.first()
        self.assertEqual(team.name, 'Test Team')
        self.assertEqual(team.description, 'A team for testing purposes')

        self.assertRedirects(response, reverse('teamdetails')) 

        def test_cancel_button_redirects(self):
            response = self.client.get(reverse('createTeam'))
        self.assertContains(response, 'Cancel')
        
        response = self.client.get('/dashboard')  
        self.assertRedirects(response, '/dashboard') 

class CTDTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        
        self.team = Team.objects.create(name="Test Team")
        
    def test_create_todo_page_accessible(self):
        response = self.client.get(reverse('createToDo'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Title')  
        self.assertContains(response, 'Description')  
        self.assertContains(response, 'Due Date')  
        self.assertContains(response, 'Category')  
        self.assertContains(response, 'Assigned to:')  

    def test_csrf_token_in_form(self):
        response = self.client.get(reverse('createToDo'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_create_todo_form_invalid(self):
        response = self.client.post(reverse('createToDo'), {
            'title': '',  
            'description': '',  
            'dueDate': '12/32/2025',  
            'category': '',  
            'team': self.team.id,  
            'assigned_to': self.user.id,  
        })

        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'description', 'This field is required.')
        self.assertFormError(response, 'form', 'dueDate', 'Please enter a valid date in MM/DD/YYYY format.')
        
    def test_create_todo_form_valid(self):
        response = self.client.post(reverse('createToDo'), {
            'title': 'Test Task',
            'description': 'Description of the test task',
            'dueDate': '12/25/2025',  
            'category': 'Test Category',
            'team': self.team.id, 
            'assigned_to': self.user.id, 
        })

        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Description of the test task')
        self.assertEqual(task.dueDate.strftime('%m/%d/%Y'), '12/25/2025')
        self.assertEqual(task.category, 'Test Category')
        self.assertEqual(task.assigned_to, self.user)

        self.assertRedirects(response, reverse('dashboard'))  

    def test_due_date_in_the_past(self):
        response = self.client.post(reverse('createToDo'), {
            'title': 'Test Task',
            'description': 'Description of the test task',
            'dueDate': '01/01/2020',
            'category': 'Test Category',
            'team': self.team.id,
            'assigned_to': self.user.id,
        })

        self.assertFormError(response, 'form', 'dueDate', 'Due date cannot be in the past.')

    def test_cancel_button_redirects(self):
        response = self.client.get(reverse('createToDo'))
        self.assertContains(response, 'Cancel')

        response = self.client.get(reverse('dashboard')) 
        self.assertRedirects(response, reverse('dashboard'))

class DashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.team = Team.objects.create(name="Test Team")
        self.task1 = Task.objects.create(
            title="Test Task 1", 
            description="This is a test task", 
            user=self.user, 
            team=self.team
        )
        self.task2 = Task.objects.create(
            title="Test Task 2", 
            description="This is another test task", 
            user=self.user, 
            team=self.team
        )
    def test_dashboard_renders_with_tasks(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test Task 1")
        self.assertContains(response, "Test Task 2")

        self.assertContains(response, "Test Team")
    
    def test_dashboard_shows_empty_message_when_no_tasks(self):
        Task.objects.all().delete()

        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, "No ToDo's available. Create a new task to get started!")

    def test_dashboard_new_todo_button_redirect(self):
        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, 'New ToDo')

        new_todo_url = reverse('todos_new')
        self.assertContains(response, f'window.location.href=\'{new_todo_url}\'')

    def test_delete_task(self):
        self.assertEqual(Task.objects.count(), 2)

        delete_url = reverse('delete', kwargs={'task_id': self.task1.id})

        response = self.client.post(delete_url)

        self.assertEqual(Task.objects.count(), 1)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

        self.assertRedirects(response, reverse('dashboard'))

    def test_timer_buttons_visibility(self):
        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, "Start")


    def test_dashboard_shows_user_specific_tasks(self):
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        new_user_task = Task.objects.create(
            title="New User Task", 
            description="Task for a new user", 
            user=new_user
        )
        self.client.login(username='newuser', password='newpassword')

        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, "New User Task")
        self.assertNotContains(response, "Test Task 1")
        self.assertNotContains(response, "Test Task 2")

    def test_dashboard_csrf_token(self):
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'csrfmiddlewaretoken')

class FPWTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.url = reverse('forgotpsw') 

    def test_forgot_password_page_renders(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'csrfmiddlewaretoken')

        self.assertContains(response, 'name="email"')

        self.assertContains(response, '<button type="submit">Forgot Password</button>')

    def test_forgot_password_with_invalid_email(self):
        response = self.client.post(self.url, {'email': 'invalid-email'}, follow=True)

        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

        self.assertContains(response, '<input type="email" name="email"')

        self.assertNotContains(response, 'Password reset email sent!')

    def test_forgot_password_with_valid_email(self):
        response = self.client.post(self.url, {'email': 'testuser@example.com'}, follow=True)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['testuser@example.com'])
        self.assertIn('Password reset', mail.outbox[0].subject)

        self.assertContains(response, 'Password reset email sent! Check your inbox.')

    def test_forgot_password_csrf_token(self):
        response = self.client.post(self.url, {'email': 'testuser@example.com'})

        self.assertEqual(response.status_code, 403)

    def test_forgot_password_message_displayed(self):
        response = self.client.post(self.url, {'email': 'testuser@example.com'}, follow=True)

        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(str(messages[0]), 'Password reset email sent! Check your inbox.')

    def test_message_popup(self):
        response = self.client.post(self.url, {'email': 'invalid-email'}, follow=True)

        self.assertContains(response, 'class="message error"')
        self.assertContains(response, 'Please enter a valid email address.') 

class LandingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.url = reverse('landingpage') 

    def test_landing_page_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DePaul University Logo') 

    def test_landing_page_navigation_logged_out(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Login')
        self.assertNotContains(response, 'Logout')

    def test_landing_page_navigation_logged_in(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.url)
        self.assertContains(response, 'Logout')
        self.assertNotContains(response, 'Login')

class LoginTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.url = reverse('login') 

    def test_login_page_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email')  
        self.assertContains(response, 'Password')  
        self.assertContains(response, 'Login') 

    def test_login_page_submit_success(self):
        response = self.client.post(self.url, {'email': 'testuser@example.com', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('home'))

    def test_login_page_submit_invalid_credentials(self):
        response = self.client.post(self.url, {'email': 'testuser@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'Invalid credentials')  

    def test_forgot_password_button(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Forgot Password?')  
        response = self.client.get('/forgotpsw')
        self.assertEqual(response.status_code, 200) 

    def test_register_button(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Register') 
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200) 

class LogoutTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.login_url = reverse('login') 
        self.logout_url = reverse('logout')

    def test_logout_redirects_to_login(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.logout_url)

        self.assertRedirects(response, self.login_url)

    def test_logged_out_user_access(self):

        response = self.client.get(reverse('landingpage'))

        self.assertRedirects(response, self.login_url)

    def test_logout_button(self):

        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.login_url)
        self.assertContains(response, 'Logout') 

    def test_logout_clears_session(self):
        self.client.login(username='testuser', password='testpassword')

        self.client.get(self.logout_url)

        response = self.client.get(reverse('landingpage')) 
        self.assertRedirects(response, self.login_url)

class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')

        self.reset_password_url = reverse('recoverPassword')  

    def test_password_reset_form_submission_valid(self):
        response = self.client.post(self.recoverPassword_url, {
            'password': 'PassWord2025#',
            'confirm-password': 'PassWord2025#'
        })
        
        self.assertRedirects(response, reverse('password_reset_done'))  

    def test_password_reset_form_mismatched_passwords(self):
        response = self.client.post(self.recoverPassword_url, {
            'password': 'PassWord2025#',
            'confirm-password': 'PassWord2025$'
        })

        self.assertFormError(response, 'form', 'confirm-password', 'Passwords do not match')

    def test_password_reset_form_too_short_password(self):
        response = self.client.post(self.recoverPassword_url, {
            'password': 'TinyPW!',
            'confirm-password': 'TinyPW!'
        })

        self.assertFormError(response, 'form', 'password', 'Password must be at least 8 characters long')

    def test_password_reset_form_missing_fields(self):
        response = self.client.post(self.recoverPassword_url, {
            'password': '',
            'confirm-password': ''
        })

        self.assertFormError(response, 'form', 'password', 'This field is required.')
        self.assertFormError(response, 'form', 'confirm-password', 'This field is required.')

    def test_password_reset_form_invalid_password_criteria(self):
        response = self.client.post(self.recoverPassword_url, {
            'password': 'nocapspass',
            'confirm-password': 'nocapspass'
        })

        self.assertFormError(response, 'form', 'password', 'Password must contain at least one uppercase letter')

        self.assertFormError(response, 'form', 'password', 'Password must contain at least one number')
        self.assertFormError(response, 'form', 'password', 'Password must contain at least one special character')

    def test_password_reset_button_click(self):
        response = self.client.get(self.recoverPassword_url)
        
        self.assertContains(response, 'Reset Password')

class RegisterTests(TestCase):
    def setUp(self):
        self.register_url = reverse('register') 

    def test_register_form_valid(self):
        response = self.client.post(self.register_url, {
            'email': 'testuser@example.com',
            'password1': 'ValidPassword123!',
            'password2': 'ValidPassword123!'
        })
        
        self.assertRedirects(response, reverse('login'))  
        
        user = User.objects.get(username='testuser@example.com')
        self.assertIsNotNone(user)
    
    def test_register_form_missing_fields(self):
        response = self.client.post(self.register_url, {
            'email': '',
            'password1': '',
            'password2': ''
        })

        self.assertFormError(response, 'form', 'email', 'This field is required.')
        self.assertFormError(response, 'form', 'password1', 'This field is required.')
        self.assertFormError(response, 'form', 'password2', 'This field is required.')

    def test_register_form_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'email': 'testuser@example.com',
            'password1': 'ValidPassword123!',
            'password2': 'DifferentPassword123!'
        })
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

    def test_register_form_password_too_short(self):
        response = self.client.post(self.register_url, {
            'email': 'testuser@example.com',
            'password1': 'short',
            'password2': 'short'
        })
        self.assertFormError(response, 'form', 'password1', 'This password is too short. It must contain at least 8 characters.')

    def test_register_form_invalid_email(self):
        response = self.client.post(self.register_url, {
            'email': 'invalidemail',
            'password1': 'ValidPassword123!',
            'password2': 'ValidPassword123!'
        })

        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_register_page_contains_form(self):
        response = self.client.get(self.register_url)
        self.assertContains(response, '<form')
        self.assertContains(response, 'email')
        self.assertContains(response, 'password1')
        self.assertContains(response, 'password2')

class TeamDetailsViewTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", email="mmccreed@depaul.edu", password="password123")
        self.member = User.objects.create_user(username="member", email="mmccreed@depaul.edu", password="password123")
        
        self.team = Team.objects.create(name="Test Team", description="Test Team Description", owner=self.owner)
        
        self.team.members.add(self.owner)
        
        self.team_url = reverse('team_details', args=[self.team.id])
        self.add_member_url = reverse('add_member', args=[self.team.id])
        self.delete_team_url = reverse('delete_team', args=[self.team.id])
        
    def test_team_details_page_renders_correctly(self):
        response = self.client.get(self.team_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Team")  
        self.assertContains(response, "Test Team Description")  
        self.assertContains(response, "Team Owner: mmccreed@depaul.edu")  
        self.assertContains(response, "mmccreed@depaul.edu") 
    
    def test_add_member_form_submission(self):
        self.client.login(username="owner", password="password123")
        
        data = {'email': 'mmccreed@depaul.edu'}
        
        self.client.post(self.add_member_url, data)
        
        self.team.refresh_from_db()
        self.assertTrue(self.team.members.filter(email='mmccreed@depaul.edu').exists())
        
    def test_add_member_duplicate(self):
        self.client.login(username="owner", password="password123")
        
        data = {'email': 'mmccreed@depaul.edu'}
        response = self.client.post(self.add_member_url, data)
        
        self.assertFormError(response, 'form', 'email', 'This user is already in this team.')
    
    def test_delete_team(self):
        self.client.login(username="owner", password="password123")
        
        response = self.client.post(self.delete_team_url, {'_method': 'DELETE'})
        
        self.assertRedirects(response, reverse('dashboard'))
        
        with self.assertRaises(Team.DoesNotExist):
            Team.objects.get(id=self.team.id)
    
    def test_error_messages_on_add_member(self):
        self.client.login(username="owner", password="password123")
        
        data = {'email': 'invalid-email'}
        
        response = self.client.post(self.add_member_url, data)
        
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_message_popup_on_success(self):
        self.client.login(username="owner", password="password123")
        
        data = {'email': 'mmccreed@depaul.edu'}
        
        response = self.client.post(self.add_member_url, data)
        
        self.assertContains(response, 'Success', status_code=200)

