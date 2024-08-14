from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve


# Create your tests here.


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        test_user = User.objects.create_user(
            username="fifi", email="fifi@example.com", password="testpass123"
        )
        self.assertEqual(test_user.username, "fifi")
        self.assertEqual(test_user.email, "fifi@example.com")
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


class SignUpPageTests(TestCase):
    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
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
