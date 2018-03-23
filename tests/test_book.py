import json
import os
import unittest

# local import
from app import create_app

class BookTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.book = {'title':'A brief history of time'}

    def test_book_creation(self):
        # Test API can create books
        resp = self.client().post('/books', data=self.book)
        self.assertEqual(resp.status_code,201)
        self.assertIn('A brief history of time', str(resp.data))

    def test_api_can_get_all_books(self):
        # Test API can get a book
        resp = self.client().post('/books/', data=self.book)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/books/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('A brief history of time', str(resp.data))

    def test_api_can_get_book_by_id(self):
        # test API can get a single book by ID
        resp = self.client().post('/books/', data=self.book)
        self.assertEqual(resp.status_code, 201)
        result_in_json = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/books/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('A brief history of time ', str(result.data))

    def test_book_deletion(self):
        # test API can delete a single book
        resp = self.client().post('/books/',data={'title':'A brief history of time'})
        self.assertEqual(resp.status_code, 201)
        rs = self.client().delete('/books/1')
        self.assertEqual(rs.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/books/1')
        self.assertEqual(result.status_code, 404)
    
    def test_books_can_be_edited(self):
        # Test API can edit an existing book
        resp = self.client().post('/books/',data={'title':'A brief history of time'})
        self.assertEqual(resp.status_code, 201)
        rs = self.client().put('/books/1',
            data={
                "name": "A very long history of time"
            })
        self.assertEqual(rs.status_code, 200)
        results = self.client().get('/books/1')
        self.assertIn('A very long history of time', str(results.data))