from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsCreator


@method_decorator(name='update', decorator=swagger_auto_schema(operation_description="Изменение привычки."))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_description="Удаление привычки."))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_description="Создание привычки."))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Информация о привычке."))
@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="Список привычек."))
class HabitViewSet(ModelViewSet):
    """Вьюсет для привычек."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_anonymous:
            if self.request.user.is_superuser:
                queryset = Habit.objects.all()
            else:
                queryset = queryset.filter(user=self.request.user)
            return queryset

    def get_permissions(self):
        if self.action != "create":
            self.permission_classes = (
                IsAuthenticated, IsCreator | IsAdminUser,
            )
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        """Частичное изменение привычки."""

        return super().partial_update(request, *args, **kwargs)


class PublicHabitListAPIView(ListAPIView):
    """Список публичных привычек."""

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer


class PublicHabitRetrieveAPIView(RetrieveAPIView):
    """Информация о публичной привычке."""

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
