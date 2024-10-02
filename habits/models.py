from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        related_name="habits",
        **NULLABLE,
    )
    place = models.CharField(
        max_length=100,
        verbose_name="Место",
        help_text="Укажите место, где вы занимаетесь",
    )
    do_at = models.DateTimeField(
        verbose_name="Дата и время выполнения",
        help_text="Укажите дату и время выполнения",
    )
    action = models.CharField(
        max_length=100,
        verbose_name="Действие",
        help_text="Укажите действие, которое вы выполняете",
    )
    is_enjoyable = models.BooleanField(
        verbose_name="Приятная ли привычка",
        help_text="Укажите, приятную ли привычку вы выполняете",
        default=False,
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку",
        related_name="related_habits",
        **NULLABLE,
    )
    periodicity = models.PositiveSmallIntegerField(
        verbose_name="Периодичность",
        help_text="Укажите периодичность выполнения привычки в днях",
        default=1,
    )
    reward = models.CharField(
        max_length=200,
        verbose_name="Вознаграждение",
        help_text="Укажите вознаграждение за выполнение привычки",
        **NULLABLE,
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name="Продолжительность",
        help_text="Укажите продолжительность выполнения действия в секундах",
    )
    is_public = models.BooleanField(
        verbose_name="Публичная ли привычка",
        help_text="Укажите, публичная ли привычка",
        default=False,
    )

    def __str__(self):
        return f"Я буду {self.action} в {self.do_at} {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
