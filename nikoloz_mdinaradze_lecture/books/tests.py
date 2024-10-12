from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase

from books.models import Book


class BookModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="<NAME>",
            publish_date="2024-10-12",
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "<NAME>")
        self.assertEqual(self.book.publish_date, "2024-10-12")

    def test_string_representation(self):
        self.assertEqual(str(self.book), "Test Book")

    def test_create_invalid_book_title(self):
        invalid_title_data = {
            "title": "A" * 101,  # max length is 100
            "author": "<NAME>",
            "publish_date": "2024-10-12",
        }
        book = Book(**invalid_title_data)
        with self.assertRaises(ValidationError):
            book.full_clean()  # This method validates model

    def test_create_invalid_book_author(self):
        invalid_author_data = {
            "title": "Test Book",
            "author": "A" * 101,
            "publish_date": "2024-10-12",
        }
        book = Book(**invalid_author_data)
        with self.assertRaises(ValidationError):
            book.full_clean()  # This method validates model


class BookTestCase(APITestCase):
    def setUp(self):
        self.book_payload = {
            "title": "Test Book",
            "author": "<NAME>",
            "publish_date": "2024-12-12"
        }
        self.list_url = reverse('book-list')
        self.book = Book.objects.create(**self.book_payload)
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})

    def test_create_book(self):
        response = self.client.post(self.list_url, data=self.book_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data['title'], self.book_payload['title'])
        self.assertEqual(response.data['author'], self.book_payload['author'])
        self.assertEqual(response.data['publish_date'], self.book_payload['publish_date'])

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_book(self):
        update_data = {
            "title": "Test Book1",
            "author": "<NAME1>",
            "publish_date": "2024-11-12"
        }
        response = self.client.put(self.detail_url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], update_data['title'])
        self.assertEqual(response.data['author'], update_data['author'])
        self.assertEqual(response.data['publish_date'], update_data['publish_date'])

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book_payload['title'])
        self.assertEqual(response.data['author'], self.book_payload['author'])
        self.assertEqual(response.data['publish_date'], self.book_payload['publish_date'])

    def test_partial_update_book(self):
        update_data = {
            "title": "Test Book1",
        }
        response = self.client.patch(self.detail_url, data=update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], update_data['title'])

    def test_delete_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
