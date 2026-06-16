from django.test import TestCase
from products.models import Category 
class CategoryModelTest(TestCase):

    def test_create_category(self):

        category = Category.objects.create(
            name="AB"
        )

        self.assertEqual(category.name, "AB")