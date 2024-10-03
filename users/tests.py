from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class UserTestCase(APITestCase):
    """Класс для тестирования пользователя"""

    def test_user_create(self):
        """Тестирование создания пользователя"""

        url = reverse("users:register")
        data = {"email": "user_1@email.com", "password": 123456}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
