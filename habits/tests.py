from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Класс для тестирования привычки."""

    maxDiff = None

    def setUp(self):
        """Метод для заполнения первичных данных."""

        # создаем админа
        self.admin_user = User.objects.create(email="admin@email.com", is_staff=True)

        # создаем обычного пользователя
        self.regular_user = User.objects.create(email="regular_user@email.com")

        # создаем создателя привычки
        self.creator_user = User.objects.create(email="creator_user@email.com")

        # создаем приятную привычку
        self.enjoyable_habit = Habit.objects.create(
            user=self.creator_user,
            place="дома",
            do_at="2024-10-05T11:35:00+03:00",
            action="лежать",
            is_enjoyable=True,
            related_habit=None,
            periodicity=1,
            reward=None,
            duration=60,
            is_public=False,
        )

        # создаем полезную привычку, связанную с приятной привычкой
        self.useful_habit_with_related_habit = Habit.objects.create(
            user=self.creator_user,
            place="дома",
            do_at="2024-10-05T11:30:00+03:00",
            action="отжиматься",
            is_enjoyable=False,
            related_habit=self.enjoyable_habit,
            periodicity=1,
            reward=None,
            duration=60,
            is_public=False,
        )

        # создаем полезную привычку с вознаграждением
        self.useful_habit_with_reward = Habit.objects.create(
            user=self.creator_user,
            place="дома",
            do_at="2024-10-05T07:00:00+03:00",
            action="делать зарядку",
            is_enjoyable=False,
            related_habit=None,
            periodicity=1,
            reward="съесть конфетку",
            duration=60,
            is_public=False,
        )

    # Тесты для админа
    def test_habit_retrieve_admin_access(self):
        """Тестирует получение информации об одной привычке админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("habits:habit-detail", args=(self.useful_habit_with_reward.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.useful_habit_with_reward.action)

    def test_habit_create_admin_access(self):
        """Тестирует создание полезной привычки с вознаграждением админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("habits:habit-list")
        data = {
            "user": self.admin_user.pk,
            "place": "в парке",
            "do_at": "2024-10-05T07:00:00+03:00",
            "action": "гулять",
            "is_enjoyable": False,
            "periodicity": 1,
            "reward": "покормить белок",
            "duration": 120,
            "is_public": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 4)

    def test_habit_update_admin_access(self):
        """Тестирует обновление информации о привычке админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "habits:habit-detail", args=(self.useful_habit_with_related_habit.pk,)
        )
        data = {"place": "на улице"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), "на улице")

    def test_habit_delete_admin_access(self):
        """Тестирует удаление привычки админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "habits:habit-detail", args=(self.useful_habit_with_related_habit.pk,)
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list_admin_access(self):
        """Тестирует получение списка привычек админом."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.enjoyable_habit.pk,
                    "duration": self.enjoyable_habit.duration,
                    "place": self.enjoyable_habit.place,
                    "do_at": self.enjoyable_habit.do_at,
                    "action": self.enjoyable_habit.action,
                    "is_enjoyable": self.enjoyable_habit.is_enjoyable,
                    "periodicity": self.enjoyable_habit.periodicity,
                    "reward": self.enjoyable_habit.reward,
                    "is_public": self.enjoyable_habit.is_public,
                    "user": self.enjoyable_habit.user.pk,
                    "related_habit": self.enjoyable_habit.related_habit,
                },
                {
                    "id": self.useful_habit_with_related_habit.pk,
                    "duration": self.useful_habit_with_related_habit.duration,
                    "place": self.useful_habit_with_related_habit.place,
                    "do_at": self.useful_habit_with_related_habit.do_at,
                    "action": self.useful_habit_with_related_habit.action,
                    "is_enjoyable": self.useful_habit_with_related_habit.is_enjoyable,
                    "periodicity": self.useful_habit_with_related_habit.periodicity,
                    "reward": self.useful_habit_with_related_habit.reward,
                    "is_public": self.useful_habit_with_related_habit.is_public,
                    "user": self.useful_habit_with_related_habit.user.pk,
                    "related_habit": self.useful_habit_with_related_habit.related_habit.pk,
                },
                {
                    "id": self.useful_habit_with_reward.pk,
                    "duration": self.useful_habit_with_reward.duration,
                    "place": self.useful_habit_with_reward.place,
                    "do_at": self.useful_habit_with_reward.do_at,
                    "action": self.useful_habit_with_reward.action,
                    "is_enjoyable": self.useful_habit_with_reward.is_enjoyable,
                    "periodicity": self.useful_habit_with_reward.periodicity,
                    "reward": self.useful_habit_with_reward.reward,
                    "is_public": self.useful_habit_with_reward.is_public,
                    "user": self.useful_habit_with_reward.user.pk,
                    "related_habit": self.useful_habit_with_reward.related_habit,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для обычного пользователя
    def test_habit_retrieve_regular_user_access(self):
        """Тестирует получение информации об одной привычке обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("habits:habit-detail", args=(self.useful_habit_with_reward.pk,))
        response = self.client.get(url)
        response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_habit_create_regular_user_access(self):
        """Тестирует создание полезной привычки с вознаграждением обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("habits:habit-list")
        data = {
            "user": self.admin_user.pk,
            "place": "в парке",
            "do_at": "2024-10-05T07:00:00+03:00",
            "action": "гулять",
            "is_enjoyable": False,
            "periodicity": 1,
            "reward": "покормить белок",
            "duration": 120,
            "is_public": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 4)

    def test_habit_update_regular_user_access(self):
        """Тестирует обновление информации о привычке обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse(
            "habits:habit-detail", args=(self.useful_habit_with_related_habit.pk,)
        )
        data = {"place": "на улице"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_habit_delete_regular_user_access(self):
        """Тестирует удаление привычки обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse(
            "habits:habit-detail", args=(self.useful_habit_with_related_habit.pk,)
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_habit_list_regular_user_access(self):
        """Тестирует получение списка привычек обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()
        result = {"count": 0, "next": None, "previous": None, "results": []}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для создателя привычки
    def test_habit_retrieve_creator_user_access(self):
        """Тестирует получение информации об одной привычке ее создателем."""

        self.client.force_authenticate(user=self.creator_user)
        url = reverse("habits:habit-detail", args=(self.useful_habit_with_reward.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.useful_habit_with_reward.action)

    def test_habit_create_creator_user_access(self):
        """Тестирует создание полезной привычки с вознаграждением ее создателем."""

        self.client.force_authenticate(user=self.creator_user)
        url = reverse("habits:habit-list")
        data = {
            "user": self.admin_user.pk,
            "place": "в парке",
            "do_at": "2024-10-05T07:00:00+03:00",
            "action": "гулять",
            "is_enjoyable": False,
            "periodicity": 1,
            "reward": "покормить белок",
            "duration": 120,
            "is_public": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 4)

    def test_habit_update_creator_user_access(self):
        """Тестирует обновление информации о привычке ее создателем."""

        self.client.force_authenticate(user=self.creator_user)
        url = reverse(
            "habits:habit-detail", args=(self.useful_habit_with_related_habit.pk,)
        )
        data = {"place": "на улице"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), "на улице")

    def test_habit_delete_creator_user_access(self):
        """Тестирует удаление привычки ее создателем."""

        self.client.force_authenticate(user=self.creator_user)
        url = reverse(
            "habits:habit-detail", args=(self.useful_habit_with_related_habit.pk,)
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list_creator_user_access(self):
        """Тестирует получение списка привычек ее создателем."""

        self.client.force_authenticate(user=self.creator_user)
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.enjoyable_habit.pk,
                    "duration": self.enjoyable_habit.duration,
                    "place": self.enjoyable_habit.place,
                    "do_at": self.enjoyable_habit.do_at,
                    "action": self.enjoyable_habit.action,
                    "is_enjoyable": self.enjoyable_habit.is_enjoyable,
                    "periodicity": self.enjoyable_habit.periodicity,
                    "reward": self.enjoyable_habit.reward,
                    "is_public": self.enjoyable_habit.is_public,
                    "user": self.enjoyable_habit.user.pk,
                    "related_habit": self.enjoyable_habit.related_habit,
                },
                {
                    "id": self.useful_habit_with_related_habit.pk,
                    "duration": self.useful_habit_with_related_habit.duration,
                    "place": self.useful_habit_with_related_habit.place,
                    "do_at": self.useful_habit_with_related_habit.do_at,
                    "action": self.useful_habit_with_related_habit.action,
                    "is_enjoyable": self.useful_habit_with_related_habit.is_enjoyable,
                    "periodicity": self.useful_habit_with_related_habit.periodicity,
                    "reward": self.useful_habit_with_related_habit.reward,
                    "is_public": self.useful_habit_with_related_habit.is_public,
                    "user": self.useful_habit_with_related_habit.user.pk,
                    "related_habit": self.useful_habit_with_related_habit.related_habit.pk,
                },
                {
                    "id": self.useful_habit_with_reward.pk,
                    "duration": self.useful_habit_with_reward.duration,
                    "place": self.useful_habit_with_reward.place,
                    "do_at": self.useful_habit_with_reward.do_at,
                    "action": self.useful_habit_with_reward.action,
                    "is_enjoyable": self.useful_habit_with_reward.is_enjoyable,
                    "periodicity": self.useful_habit_with_reward.periodicity,
                    "reward": self.useful_habit_with_reward.reward,
                    "is_public": self.useful_habit_with_reward.is_public,
                    "user": self.useful_habit_with_reward.user.pk,
                    "related_habit": self.useful_habit_with_reward.related_habit,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

        # Тесты для анонимного пользователя

    def test_habit_retrieve_anonymous_user_access(self):
        """Тестирует получение информации об одной привычке анонимным пользователем."""

        url = reverse("habits:habit-detail", args=(self.useful_habit_with_reward.pk,))
        response = self.client.get(url)
        response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_create_anonymous_user_access(self):
        """Тестирует создание полезной привычки с вознаграждением анонимным пользователем."""

        url = reverse("habits:habit-list")
        data = {
            "user": self.admin_user.pk,
            "place": "в парке",
            "do_at": "2024-10-05T07:00:00+03:00",
            "action": "гулять",
            "is_enjoyable": False,
            "periodicity": 1,
            "reward": "покормить белок",
            "duration": 120,
            "is_public": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_update_anonymous_user_access(self):
        """Тестирует обновление информации о привычке анонимным пользователем."""

        url = reverse(
            "habits:habit-detail", args=(self.useful_habit_with_related_habit.pk,)
        )
        data = {"place": "на улице"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_delete_anonymous_user_access(self):
        """Тестирует удаление привычки анонимным пользователем."""

        url = reverse(
            "habits:habit-detail", args=(self.useful_habit_with_related_habit.pk,)
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_habit_list_anonymous_user_access(self):
        """Тестирует получение списка привычек анонимным пользователем."""

        url = reverse("habits:habit-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Тесты для проверки валидаторов
    def test_habit_create_RelatedHabitOrRewardValidator_error(self):
        """Тестирует ошибку при создании привычки с одновременным указанием связанной привычки и вознаграждения."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("habits:habit-list")
        data = {
            "user": self.admin_user.pk,
            "place": "в парке",
            "do_at": "2024-10-05T07:00:00+03:00",
            "action": "гулять",
            "is_enjoyable": False,
            "related_habit": self.enjoyable_habit.pk,
            "periodicity": 1,
            "reward": "покормить белок",
            "duration": 120,
            "is_public": False,
        }
        self.client.post(url, data)

        self.assertRaises(ValidationError)

    def test_user_create_validate_duration_error(self):
        """Тестирует ошибку при создании привычки с временем выполнения больше 120 секунд."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("habits:habit-list")
        data = {
            "user": self.admin_user.pk,
            "place": "в парке",
            "do_at": "2024-10-05T07:00:00+03:00",
            "action": "гулять",
            "is_enjoyable": False,
            "related_habit": self.enjoyable_habit.pk,
            "periodicity": 1,
            "duration": 200,
            "is_public": False,
        }
        self.client.post(url, data)

        self.assertRaises(ValidationError)

    def test_habit_create_RelatedHabitValidator_error(self):
        """Тестирует ошибку при создании привычки, связанной с привычкой не являющейся приятной."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("habits:habit-list")
        data = {
            "user": self.admin_user.pk,
            "place": "в парке",
            "do_at": "2024-10-05T07:00:00+03:00",
            "action": "гулять",
            "is_enjoyable": False,
            "related_habit": self.useful_habit_with_related_habit.pk,
            "periodicity": 1,
            "duration": 120,
            "is_public": False,
        }
        self.client.post(url, data)

        self.assertRaises(ValidationError)

    def test_habit_create_EnjoyableHabitValidator_error(self):
        """Тестирует ошибку при создании приятной привычки с вознаграждением."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("habits:habit-list")
        data = {
            "user": self.admin_user.pk,
            "place": "в парке",
            "do_at": "2024-10-05T07:00:00+03:00",
            "action": "гулять",
            "is_enjoyable": True,
            "periodicity": 1,
            "reward": "покормить белок",
            "duration": 120,
            "is_public": False,
        }
        self.client.post(url, data)

        self.assertRaises(ValidationError)

    def test_habit_create_PeriodicityValidator_error(self):
        """Тестирует ошибку при создании привычки с периодичностью выполнения реже, чем 1 раз в 7 дней."""

        self.client.force_authenticate(user=self.admin_user)
        url = reverse("habits:habit-list")
        data = {
            "user": self.admin_user.pk,
            "place": "в парке",
            "do_at": "2024-10-05T07:00:00+03:00",
            "action": "гулять",
            "is_enjoyable": False,
            "periodicity": 10,
            "reward": "покормить белок",
            "duration": 120,
            "is_public": False,
        }
        self.client.post(url, data)

        self.assertRaises(ValidationError)
        self.assertRaisesMessage(
            ValidationError, "Нельзя выполнять привычку реже 1 раза в 7 дней."
        )


class PublicHabitTestCase(APITestCase):
    """Класс для тестирования публичной привычки."""

    maxDiff = None

    def setUp(self):
        """Метод для заполнения первичных данных."""

        # создаем обычного пользователя
        self.regular_user = User.objects.create(email="regular_user@email.com")

        # создаем создателя привычки
        self.creator_user = User.objects.create(email="creator_user@email.com")

        # создаем публичную привычку
        self.public_habit = Habit.objects.create(
            user=self.creator_user,
            place="дома",
            do_at="2024-10-05T07:00:00+03:00",
            action="делать зарядку",
            is_enjoyable=False,
            related_habit=None,
            periodicity=1,
            reward="съесть конфетку",
            duration=60,
            is_public=True,
        )

    # тесты для авторизованного пользователя
    def test_public_habit_retrieve_regular_user_access(self):
        """Тестирует получение информации об одной публичной привычке обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("habits:public-retrieve", args=(self.public_habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.public_habit.action)

    def test_public_habit_list_regular_user_access(self):
        """Тестирует получение информации об одной публичной привычке обычным пользователем."""

        self.client.force_authenticate(user=self.regular_user)
        url = reverse("habits:public-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.public_habit.pk,
                "duration": self.public_habit.duration,
                "place": self.public_habit.place,
                "do_at": self.public_habit.do_at,
                "action": self.public_habit.action,
                "is_enjoyable": self.public_habit.is_enjoyable,
                "periodicity": self.public_habit.periodicity,
                "reward": self.public_habit.reward,
                "is_public": self.public_habit.is_public,
                "user": self.public_habit.user.pk,
                "related_habit": self.public_habit.related_habit,
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

        # тесты для анонимного пользователя

    def test_public_habit_retrieve_anonymous_user_access(self):
        """Тестирует получение информации об одной публичной привычке анонимным пользователем."""

        url = reverse("habits:public-retrieve", args=(self.public_habit.pk,))
        response = self.client.get(url)
        response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_public_habit_list_anonymous_user_access(self):
        """Тестирует получение информации об одной публичной привычке анонимным пользователем."""

        url = reverse("habits:public-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
