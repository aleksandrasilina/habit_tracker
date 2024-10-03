from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsCreator


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
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


class PublicHabitListAPIView(ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer


class PublicHabitRetrieveAPIView(RetrieveAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
