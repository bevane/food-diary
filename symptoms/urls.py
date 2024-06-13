from django.urls import path
from . import views

app_name = "symptoms"
urlpatterns = [
    path("", views.index, name="index"),
    path("autocomplete_symptoms", views.autocomplete_symptoms, name="autocomplete_symptoms")
]
