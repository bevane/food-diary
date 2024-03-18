from django.db import models
from django.conf import settings

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.name}"


class FoodLog(models.Model):
    datetime = models.DateTimeField()
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.id}: {self.food.name} logged by {self.user} on {self.datetime}"
