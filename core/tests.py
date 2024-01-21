from django.test import TestCase
from rest_framework.test import APIClient
from .models import Book

class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'bookImageUrl': 'https://example.com/test.jpg'
        }
        self.book = Book.objects.create(**self.book_data)
        self.url = '/api/books/'

    def test_create_book(self):
        response = self.client.post(self.url, self.book_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)

    def test_read_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_read_book_detail(self):
        response = self.client.get(f'{self.url}{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        updated_data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'bookImageUrl': 'https://example.com/updated.jpg'
        }
        response = self.client.put(f'{self.url}{self.book.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_partial_update_book(self):
        partial_data = {'title': 'Partial Update'}
        response = self.client.patch(f'{self.url}{self.book.id}/', partial_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Partial Update')

    def test_delete_book(self):
        response = self.client.delete(f'{self.url}{self.book.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 0)
