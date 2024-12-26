import datetime
from datetime import timedelta

import pytz
import requests
from celery import shared_task
from django.utils import timezone

from config import settings
from habits.models import Habit


@shared_task
def send_telegram_message(chat_id, message):
    """Функция отправки уведомления в телеграм."""

    params = {
        "chat_id": chat_id,
        "text": message,
    }
    requests.get(
        f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage", params=params
    )


@shared_task
def send_habit_reminder():
    """Отправляет напоминания пользователю в телеграм о необходимости выполнить полезную привычку
    за 5 мин до ее начала, в момент выполнения, а также напоминание о приятной привычке или вознаграждении."""

    # current_datetime = timezone.localtime(timezone.now())
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.datetime.now(zone)

    habits = Habit.objects.filter(
        do_at__lte=current_datetime + timedelta(minutes=5),
        do_at__gt=current_datetime,
        is_enjoyable=False,
    )
    if habits:
        for habit in habits:
            message_1 = f"{habit.user.first_name if habit.user.first_name else habit.user.email}, через 5 минут пора {habit.action} {habit.place}! ({timezone.localtime(habit.do_at).strftime("%d.%m.%Y %H:%M")})"
            message_2 = f"Время {habit.action}!"
            if habit.user.tg_chat_id:
                # Отправка напоминания за 5 мин до начала привычки
                send_telegram_message(habit.user.tg_chat_id, message_1)
                habit.do_at += timedelta(days=habit.periodicity)
                habit.save()

                # Отправка напоминания о начале привычки
                send_telegram_message.apply_async(
                    args=[habit.user.tg_chat_id, message_2], countdown=60
                )

                # Отправка напоминания о выполнении приятной привычки при ее наличии
                if habit.related_habit:
                    enjoyable_habit = habit.related_habit
                    message = f"Ты молодец! Настало время сделать что-то приятное. Пора {enjoyable_habit.action}!"
                    send_telegram_message.apply_async(
                        args=[habit.user.tg_chat_id, message],
                        countdown=(habit.duration + 5 * 60),
                    )

                # Отправка напоминания о вознаграждении при его наличии
                else:
                    message = f"Ты молодец! Настало время сделать что-то приятное. Пора {habit.reward}!"
                    send_telegram_message.apply_async(
                        args=[habit.user.tg_chat_id, message],
                        countdown=(habit.duration + 5 * 60),
                    )
            else:
                print("Укажите свой tg_chat_id для рассылки напоминаний")
