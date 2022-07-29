from rest_framework.test import APITestCase, APIClient

from .models import Product

class ProductCreateTestCase(APITestCase):
#     def setUp(self):

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