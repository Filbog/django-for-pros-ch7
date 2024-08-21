from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class CustomUserTests(TestCase):

    def setUp(self):
        # Set up the site and social app, if necessary
        site = Site.objects.get_or_create(name="example.com", domain="example.com")[0]

        social_app = SocialApp.objects.create(
            provider="github", name="github", client_id="123", secret="1234567890"
        )
        social_app.sites.add(site)

        # Create a user for login tests
        User = get_user_model()
        self.user = User.objects.create_user(
            username="fifi", email="fifi@example.com", password="testpass123"
        )

    def test_create_user(self):
        User = get_user_model()
        test_user = User.objects.create_user(
            username="fifi2", email="fifi2@example.com", password="testpass123"
        )
        self.assertEqual(test_user.username, "fifi2")
        self.assertEqual(test_user.email, "fifi2@example.com")
        self.assertTrue(test_user.is_active)
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="test_admin", email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(admin_user.username, "test_admin")
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_login_user(self):
        # Log in with the test user
        login = self.client.login(email="fifi@example.com", password="testpass123")
        self.assertTrue(login)  # Check that the login was successful

        # Optionally, you can also verify that the user is logged in by accessing a view that requires authentication
        response = self.client.get(
            reverse("book_list")
        )  # Replace with a view that requires login
        self.assertEqual(
            response.status_code, 200
        )  # Should return 200 if the user is logged in


class SignUpPageTests(TestCase):
    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
        # not sure if all this is necessary if we have social auth enabled, or just stems from my small mistake of deleting the default Site in Django Admin XDDD
        site = Site.objects.get_or_create(name="example.com", domain="example.com")[0]

        social_app = SocialApp.objects.create(
            provider="github", name="github", client_id="123", secret="1234567890"
        )
        social_app.sites.add(site)

        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "I should not be on this page")

    def test_signup_form(self):
        create_new_user = get_user_model().objects.create_user(
            self.username, self.email
        )
        all_users = get_user_model().objects.all()
        self.assertEqual(all_users.count(), 1)
        self.assertEqual(all_users[0].username, self.username)
        self.assertEqual(all_users[0].email, self.email)
