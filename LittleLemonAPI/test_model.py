from django.test import TestCase
from .models import Menu
# Create your tests here.

class MenuItemTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(name='TestItem', price=10, menu_item_description='TestDescription')
        self.assertEqual(item.name, 'TestItem')
        self.assertEqual(item.price, 10)
        self.assertEqual(item.menu_item_description, 'TestDescription')
