from django.db import models
from django.conf import settings

# Create your models here.
class Symptoms(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class SymptomsLog(models.Model):
    datetime = models.DateTimeField()
    symptom = models.ForeignKey(
        Symptoms,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.id}: {self.symptom.name} logged by {self.user} on {self.datetime}"
