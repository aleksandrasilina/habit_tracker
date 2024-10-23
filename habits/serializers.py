from rest_framework import serializers

from habits.models import Habit
from habits.validators import (EnjoyableHabitValidator, PeriodicityValidator,
                               RelatedHabitOrRewardValidator,
                               RelatedHabitValidator, validate_duration)


class HabitSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(validators=[validate_duration])

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RelatedHabitOrRewardValidator(field_1="related_habit", field_2="reward"),
            RelatedHabitValidator(field="related_habit"),
            EnjoyableHabitValidator(
                is_enjoyable="is_enjoyable",
                related_habit="related_habit",
                reward="reward",
            ),
            PeriodicityValidator(field="periodicity"),
        ]
