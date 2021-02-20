from django.test import TestCase
from rest_framework.test import APIClient
from .models import Transactions

# Create your tests here.
class TransactionTestCase(TestCase):
    def setUp(self):
        self.request_handle = APIClient()
        Transactions.objects.create(payer="test", points=500)
        Transactions.objects.create(payer="test1", points=300)
    
    def test_add_transaction_with_data(self):
        post_body = {"payer": "test", "points": 1000}
        response = self.request_handle.post('/add-transaction/', post_body)
        self.assertEqual(response.data, {"Details":"Success"})
        self.assertEqual(response.status_code, 200)

    def test_add_transaction_without_data(self):
        post_body = {}
        response = self.request_handle.post('/add-transaction/', post_body)
        self.assertEqual(response.data, {"Error":"Bad details"})
        self.assertEqual(response.status_code, 400)
    
    def test_get_points_balances(self):
        dummy_data = {'test': 500, 'test1': 300}
        response = self.request_handle.get('/all-points/')
        self.assertEqual(response.data, dummy_data)
        self.assertEqual(response.status_code, 200)

    def test_spend_transaction(self):
        spend_points = {"points" : 500}
        dummy_output = [{"payer": "test", "points": -500}]
        response = self.request_handle.post('/spend-points/', spend_points)
        self.assertEqual(response.data, dummy_output)
        self.assertEqual(response.status_code, 200)

    def test_spend_transaction_zero_points(self):
        spend_points = {"points" : 0}
        dummy_output = []
        response = self.request_handle.post('/spend-points/', spend_points)
        self.assertEqual(response.data, dummy_output)
        self.assertEqual(response.status_code, 200)