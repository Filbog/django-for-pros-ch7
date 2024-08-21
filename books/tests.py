from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from .models import Book, Review

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class BookTests(TestCase):

    def setUp(self):
        # not sure if all this is necessary if we have social auth enabled, or just stems from my small mistake of deleting the default Site in Django Admin XDDD
        site = Site.objects.get_or_create(name="example.com", domain="example.com")[0]

        social_app = SocialApp.objects.create(
            provider="github", name="github", client_id="123", secret="1234567890"
        )
        social_app.sites.add(site)

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reviewuser", email="reviewbrah@gmail.com", password="password123"
        )
        cls.user.set_password("password123")
        cls.user.save()

        cls.special_permission = Permission.objects.get(
            codename="special_status",
        )

        cls.book = Book.objects.create(
            title="Harry Potter",
            author="JK Rowling",
            price="25.00",
        )

        cls.review = Review.objects.create(
            book=cls.book,
            author=cls.user,
            review="great book, kudos bruv",
        )

    def test_book_listing(self):
        self.assertEqual(f"{self.book.title}", "Harry Potter")
        self.assertEqual(f"{self.book.author}", "JK Rowling")
        self.assertEqual(f"{self.book.price}", "25.00")

    def test_book_list_view_for_logged_in_user(self):
        login = self.client.login(email="reviewbrah@gmail.com", password="password123")
        self.assertTrue(login)
        response = self.client.get(reverse("book_list"))
        print(response)
        self.assertEqual(response.status_code, 200)
        print(response)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "%s?next=/books/" % (reverse("account_login")))
        response = self.client.get("%s?next=/books/" % (reverse("account_login")))
        self.assertContains(response, "Log In")

    def test_book_detail_view_with_permissions(self):
        self.client.login(email="reviewbrah@gmail.com", password="password123")
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get("/books/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "great book, kudos bruv")
        self.assertTemplateUsed(response, "books/book_detail.html")
