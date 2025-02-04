from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from models import Team;
from models import TeamMember;
from models import Task; 

class AboutPageTests(TestCase):

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

class CreateTeamPageTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    #test page elements
    def test_create_team_page_accessible(self):
        response = self.client.get(reverse('createTeam'))  # adjust the URL name as needed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Team Name')  # Ensure the page contains the 'Team Name' field
        self.assertContains(response, 'Description')  # Ensure the page contains the 'Description' field

    def test_csrf_token_in_form(self):
        # Test if the CSRF token is present in the form
        response = self.client.get(reverse('createTeam'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_create_team_form_invalid(self):
        # Test form submission with invalid data
        response = self.client.post(reverse('createTeam'), {
            'name': '',  # Empty name
            'description': '',  # Empty description
        })

        # Ensure the form is returned with errors
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'description', 'This field is required.')

        def test_create_team_form_valid(self):
        # Test form submission with valid data
            response = self.client.post(reverse('createTeam'), {
            'name': 'Test Team',
            'description': 'A team for testing purposes',
        })

        # Check if the team is created in the database
        self.assertEqual(Team.objects.count(), 1)
        team = Team.objects.first()
        self.assertEqual(team.name, 'Test Team')
        self.assertEqual(team.description, 'A team for testing purposes')

        # Check if the response redirects to the team list page or the appropriate URL
        self.assertRedirects(response, reverse('teamdetails'))  # Adjust the redirect URL as needed

        def test_cancel_button_redirects(self):
        # Test that clicking "Cancel" redirects to the dashboard
            response = self.client.get(reverse('createTeam'))
        self.assertContains(response, 'Cancel')
        
        # Simulate clicking the cancel button by navigating directly
        response = self.client.get('/dashboard')  # Adjust URL as needed
        self.assertRedirects(response, '/dashboard')  # Adjust expected redirect as needed