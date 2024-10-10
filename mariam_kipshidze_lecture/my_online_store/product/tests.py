from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from product.models import Product
from product.serializers import ProductListSerializer


class ProductListTests(TestCase):

    def setUp(self):
        # Create initial test data
        Product.objects.create(title='Product 1', price=10.00)
        Product.objects.create(title='Product 2', price=15.00)
        Product.objects.create(title='Product 3', price=10.00)
        Product.objects.create(title='Product 4', price=15.00)

    @staticmethod
    def get_price(price, quantity, discount):
        price = price * quantity
        price = (price * (100 - discount)) / 100
        return Decimal(price)

    def test_product_list_api(self):
        # Use the test client to simulate a GET request to the product list API
        response = self.client.get('/product/product/product_list/')  # Directly using the URL path

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the expected products
        self.assertEqual(len(response.data), 4)  # Check the number of products
        self.assertEqual(response.data[0]['title'], 'Product 1')
        self.assertEqual(response.data[1]['title'], 'Product 2')
        self.assertEqual(response.data[2]['price'], '10.00')
        self.assertEqual(response.data[3]['price'], '15.00')

        # Assert that the response data matches the products in the database
        products = Product.objects.order_by('id')
        serializer_data = [ProductListSerializer(product).data for product in products]
        self.assertEqual(response.data, serializer_data)

        for product in products:
            self.assertEqual(product.get_price(quantity=2, discount=10),
                             self.get_price(price=product.price, quantity=2, discount=10))
