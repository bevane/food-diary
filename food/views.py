from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from .models import Food, FoodLog
from datetime import datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.serializers import serialize

# Create your views here.
@login_required
def index(request):
    food_history = FoodLog.objects.filter(user=request.user)
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
            food = Food(name=food_name, added_by=request.user.username)
            food.save()
        new_log = FoodLog(
            datetime=log_datetime_utc,
            food=food,
            user = request.user,
        )
        new_log.save()
        return HttpResponseRedirect(reverse("food:index"))

    return render(request, "food/index.html", {"food_history": food_history})


@login_required
def autocomplete_foods(request):
    """
    Provides autocomplete suggestions for food logging
    """
    # only allow ajax requests
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponseForbidden("403 Forbidden")
    query = request.GET.get("term", "")
    suggested_foods = list(Food.objects.filter(
        (Q(added_by=request.user) | Q(added_by="admin(fdc)"))
         & Q(name__contains=query)
    ).values("name", "added_by"))
    # sort the suggestions so that the foods added by the user will always
    # be at the top and then it will be sorted by length which will result
    # in exact matches to the search term showing up at the top
    sorted_suggestions = sorted(
        suggested_foods, key=lambda item: (
            # use not equals as the sort will be in asc order which means
            # false (0) will be at the top of the list
            item["added_by"] != request.user.username,
            len(item["name"])
            )
        # truncate sorted suggestions so that only a limited number of suggestions
        # will be shown in front end and prevent slow performance
    )[:5]
    sorted_suggestions_arr = [item["name"] for item in sorted_suggestions]
    return JsonResponse(sorted_suggestions_arr, safe=False)

