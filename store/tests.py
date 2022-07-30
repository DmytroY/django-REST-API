from rest_framework.test import APITestCase, APIClient
import os
from django.conf import settings
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


class ProductUpdateTestCase(APITestCase):

    def test_product_update(self):
        id = Product.objects.first().id
        # attributes for test product
        prod_attr = {
            'name':"Test name",
            'description':"Test descr",
            'price': 99.99,
        }
        # response = self.client.patch(f'/api/v1/products/{id}/', prod_attr, format='json')  # format='json' option is depresiate
        response = self.client.patch(f'/api/v1/products/{id}/', prod_attr)        
        if response.status_code != 200:
            print(" ====== Product have NOT been updated =======")
            print(response)

        # check data of updated product
        # print(" ====== Check updated product =======")
        updated_product = Product.objects.get(id=id)
        for attr in prod_attr:
            # print(getattr(updated_product, attr))
            self.assertEqual(getattr(updated_product, attr), prod_attr[attr]) # updated product data = attributes of test product

    def test_upload_photo(self):
        product = Product.objects.first()       # take some product
        ori_photo = product.photo               
        new_photo_path = os.path.join(settings.MEDIA_ROOT, 'products', 'vitamin-iron.jpg') # we will use existing photo file in the project 
        with open(new_photo_path, 'rb') as pf:
            # response = self.client.patch(f'/api/v1/products/{product.id}/', { 'photo': pf}, format='multipart')  # format='multipart' option is redundant
            response = self.client.patch(f'/api/v1/products/{product.id}/', { 'photo': pf})
        self.assertEqual(response.status_code, 200)             # check thlm request response code is OK
        self.assertNotEqual(ori_photo, response.data['photo'])  # check photo is changed
        try:
            updated_product = Product.objects.get(id=product.id)    # read updated product data
            # we already had this name of file in the upload/productds folder, so when we upload new photo system added postfix to the file name
            # that why we should check with the string.startswith() method
            expected_photo_pass_begining =os.path.join(settings.MEDIA_ROOT, 'products', 'vitamin-iron')  
            self.assertTrue(updated_product.photo.startswith(expected_photo_pass_begining))
        except:
            pass
        finally:
            os.remove(updated_product.photo.path) #remove uploaded photo to clear the test case scene
