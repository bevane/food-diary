from django.contrib import admin
from .models import Symptoms, SymptomsLog

# Register your models here.
admin.site.register(Symptoms)
admin.site.register(SymptomsLog)