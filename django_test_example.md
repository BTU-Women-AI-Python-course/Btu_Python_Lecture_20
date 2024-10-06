# Django Tests

## Example: Testing a Product List API with ModelViewSet

### 1. Models

Define a `Product` model in your application.

**File: `yourapp/models.py`**

```python
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
```

### 2. Serializers

Create a serializer for the `Product` model.

**File: `yourapp/serializers.py`**

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

### 3. ViewSet

Create a `ModelViewSet` for the `Product` model.

**File: `yourapp/views.py`**

```python
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

### 4. URLs

Set up the URLs for your API.

**File: `yourapp/urls.py`**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

### 5. Fixtures

Create a fixture file containing initial data for your tests.

**File: `yourapp/fixtures/product_fixture.json`**

```json
[
    {
        "model": "yourapp.product",
        "pk": 1,
        "fields": {
            "title": "Product 1",
            "price": "10.00"
        }
    },
    {
        "model": "yourapp.product",
        "pk": 2,
        "fields": {
            "title": "Product 2",
            "price": "15.00"
        }
    }
]
```

### 6. Testing

Create a test case that utilizes `TestCase`, assertions, fixtures, and the client.

**File: `yourapp/tests.py`**

```python
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from .models import Product

class ProductListTests(TestCase):

    def setUp(self):
        # Create initial test data
        Product.objects.create(title='Product 1', price=10.00)
        Product.objects.create(title='Product 2', price=15.00)

    def test_product_list_api(self):
        # Use the test client to simulate a GET request to the product list API
        response = self.client.get('/products/')  # Directly using the URL path

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the expected products
        self.assertEqual(len(response.data), 2)  # Check the number of products
        self.assertEqual(response.data[0]['title'], 'Product 1')
        self.assertEqual(response.data[1]['title'], 'Product 2')

        # Assert that the response data matches the products in the database
        products = Product.objects.all()
        serializer_data = [ProductSerializer(product).data for product in products]
        self.assertEqual(response.data, serializer_data)
```

### 7. Running the Tests

To run the tests, execute the following command in your terminal:

```bash
python manage.py test yourapp
```

### Summary of Key Concepts Used

- **TestCase**: The `ProductListTests` class inherits from `TestCase`, allowing us to create a series of tests for our product listing functionality.
- **Assertions**: We use assertions such as `assertEqual` and checks on the response status to verify the correctness of our API.
- **Fixtures**: The `fixtures` attribute loads the predefined data from `product_fixture.json` before each test, ensuring a consistent starting state.
- **Client**: The `self.client` simulates a web browser, allowing us to make requests to our API endpoint and test its responses.

This example demonstrates how to test a RESTful API endpoint using Django REST Framework's `ModelViewSet`.

In Django, when you run tests, a separate test database is automatically created to ensure that your tests do not interfere with your production or development databases. Here's a brief overview:

### Test Database in Django

1. **Creation**:
   - When you run tests using the `python manage.py test` command, Django creates a new test database (usually with the suffix `_test` added to your existing database name).

2. **Isolation**:
   - The test database is isolated from your main database, ensuring that any data created during tests (e.g., models, migrations) does not affect your actual application data.

3. **Transactions**:
   - Each test runs within a transaction that is rolled back at the end of the test. This means that any changes made to the database during a test are undone, keeping the database clean for subsequent tests.

4. **Fixtures and Data**:
   - You can load fixtures into the test database using the `fixtures` attribute in your test case, or you can create data in the `setUp` method as shown in the previous example.

5. **Speed**:
   - Since tests often create and destroy data frequently, having a separate test database speeds up testing by preventing clutter in your development or production database.

6. **Configuration**:
   - The test database configuration is usually specified in your `settings.py` file under the `DATABASES` setting. By default, it uses the same database engine and settings as your main database.
