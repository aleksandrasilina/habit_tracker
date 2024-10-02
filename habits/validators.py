from rest_framework.serializers import ValidationError


class RelatedHabitOrRewardValidator:
    """Исключает одновременный выбор связанной привычки и указания вознаграждения."""

    def __init__(self, field_1, field_2):
        self.field_1 = field_1
        self.field_2 = field_2

    def __call__(self, value):
        related_habit = dict(value).get(self.field_1)
        reward = dict(value).get(self.field_2)
        if related_habit and reward:
            raise ValidationError("Нельзя одновременно указывать и вознаграждение и связанную привычку.")


def validate_duration(value):
    """Проверяет, что время выполнения привычки не больше 120 секунд."""

    if value > 120:
        raise ValidationError("Время выполнения привычки должно быть не больше 120 секунд.")


class RelatedHabitValidator:
    """Проверяет, что в связанные привычки могут попадать только привычки с признаком приятной привычки."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val:
            if not tmp_val.is_enjoyable:
                raise ValidationError("Связанная привычка должна быть приятной.")


class EnjoyableHabitValidator:
    """Проверяет, что у приятной привычки нет вознаграждения или связанной привычки."""

    def __init__(self, is_enjoyable, related_habit, reward):
        self.is_enjoyable = is_enjoyable
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, value):
        tmp_is_enjoyable = dict(value).get(self.is_enjoyable)
        tmp_related_habit = dict(value).get(self.related_habit)
        tmp_reward = dict(value).get(self.reward)
        if tmp_is_enjoyable:
            if tmp_related_habit or tmp_reward:
                raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")


class PeriodicityValidator:
    """Проверяет, что периодичность выполнения привычки не реже, чем 1 раз в 7 дней."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val:
            if tmp_val > 7:
                raise ValidationError("Нельзя выполнять привычку реже 1 раза в 7 дней.")
