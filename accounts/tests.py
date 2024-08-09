from django.test import TestCase
from django.contrib.auth import get_user_model

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
