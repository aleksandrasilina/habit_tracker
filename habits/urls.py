from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import (HabitViewSet, PublicHabitListAPIView,
                          PublicHabitRetrieveAPIView)

app_name = HabitsConfig.name

router = SimpleRouter()
router.register("", HabitViewSet)

urlpatterns = [
    path("public/", PublicHabitListAPIView.as_view(), name="public-list"),
    path(
        "public/<int:pk>/", PublicHabitRetrieveAPIView.as_view(), name="public-retrieve"
    ),
]
urlpatterns += router.urls
