from rest_framework.test import APITestCase, APIClient

from .models import Product


class ProductCreateTestCase(APITestCase):

    def test_create_product(self):
        initial_product_count = Product.objects.count()  # How many products already are in the db?

        # attributes for test product
        prod_attr = {
            'name':"Test name",
            'description':"Test descr",
            'price': '99.99'
        }
        # in case of success self.client.post will return status and new created product data
        response = self.client.post('/api/v1/products/new', prod_attr)
        if response.status_code != 201:
            print(" ====== Product are not created =======")
            print(response)
            print(response.data)

        self.assertEqual(Product.objects.count(), initial_product_count + 1) # db product count increased with new one

        for attr in prod_attr:
            self.assertEqual(response.data[attr], prod_attr[attr]) # created product data = attributes of test product

        # check other fields and methods
        self.assertEqual(response.data['sale_start'], None)
        self.assertEqual(response.data['sale_end'], None)
        self.assertEqual(response.data['is_on_sale'], False)
        self.assertEqual(response.data['current_price'], float(response.data['price'])) # current_price should be equal to price for new created product


class ProductDestroyTestCase(APITestCase):

    def test_delete_product(self):
        initial_product_count = Product.objects.count()  # How many products are in the db?
        id = Product.objects.first().id
        response = self.client.delete(f'/api/v1/products/{id}/')
        if response.status_code != 204:
            print(" ====== Product have NOT been deleted =======")
            print(response)
            print(response.data)

        self.assertEqual(Product.objects.count(), initial_product_count - 1)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=id)

class ProductListTestCase(APITestCase):

    def test_Product_list(self):
        product_count = Product.objects.count()
        response = self.client.get('/api/v1/products/')
        if response.status_code != 200:
            print(" ====== Product list test fail =======")
            print(response)
            print(response.data)

        self.assertEqual(product_count, response.data['count'])
        self.assertEqual(product_count, len(response.data['results']))
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['next'], None)