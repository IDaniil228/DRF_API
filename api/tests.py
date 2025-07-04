from django.urls import reverse

from django.test import TestCase
from rest_framework.status import *

from api.models import User, Order


class UserOrdersTestCase(TestCase):
    def setUp(self):
        user_1 = User.objects.create_user(username="Daniil")
        order_1 = Order.objects.create(user=user_1)
        order_2 = Order.objects.create(user=user_1)
        order_3 = Order.objects.create(user=user_1)

    def test_correct_orders_fro_auth_users(self):
        user = User.objects.get(username="Daniil")
        self.client.force_login(user)
        response = self.client.get(reverse("user-orders"))

        assert response.status_code == HTTP_200_OK

        orders = response.json()
        self.assertTrue(all(order["user"] == user.id for order in orders))

    def test_for_anonymous_user(self):
        response = self.client.get(reverse("user-orders"))
        self.assertEquals(response.status_code, HTTP_403_FORBIDDEN)