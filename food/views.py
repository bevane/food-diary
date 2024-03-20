from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Food, FoodLog
from datetime import datetime, timedelta, timezone

# Create your views here.
def index(request):
    registered_foods = Food.objects.all()
    if request.method == "POST":
        food_name = request.POST["food_name"]
        # datetime from form is in iso format
        log_datetime_iso = request.POST["food-log-datetime"]
        utc_offset = request.POST["food-log-utc-offset"]
        log_datetime = datetime.fromisoformat(log_datetime_iso)
        # add utc offset to get the datetime in utc
        # because log_datetime is in user's local timezone
        log_datetime_utc = log_datetime + timedelta(minutes=int(utc_offset))
        # set tzinfo to make the datetime timezone aware
        log_datetime_utc = log_datetime_utc.replace(tzinfo=timezone.utc)
        # check if food_name already exists in db and get it if it does
        # or create a new Food if it does not exist
        try:
            food = Food.objects.get(name=food_name)
        except Food.DoesNotExist:
            food = Food(name=food_name)
            food.save()
        new_log = FoodLog(
            datetime=log_datetime_utc,
            food=food,
            user = request.user,
        )
        new_log.save()
        return HttpResponseRedirect(reverse("food:index"))

    return render(request, "food/index.html", {
        "registered_foods": registered_foods,
    })
