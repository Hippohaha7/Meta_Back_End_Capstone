from django.test import TestCase
from .models import Menu
from .views import menu_list
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User


class MenuListViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass'
        )
        self.menu = Menu.objects.create(name='Burger', price=10, menu_item_description='Delicious burger')

    def test_menu_list_view_GET(self):
        request = self.factory.get('/menu/')
        force_authenticate(request, user=self.user)
        response = menu_list(request)
        self.assertEqual(response.status_code, 200)

    def test_menu_list_view_POST(self):
        data = {'name': 'Pizza', 'price': 15, 'menu_item_description': 'Yummy pizza'}
        request = self.factory.post('/menu/', data)
        force_authenticate(request, user=self.user)
        response = menu_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Menu.objects.filter(name='Pizza').exists())