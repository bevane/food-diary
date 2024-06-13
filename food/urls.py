from django.urls import path
from . import views

app_name = "food"
urlpatterns = [
    path("", views.index, name="index"),
    path("autocomplete_foods", views.autocomplete_foods, name="autocomplete_foods")
]

