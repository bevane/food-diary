from django.shortcuts import render
from django.http import  HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from .models import Symptoms, SymptomsLog
from datetime import datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required
def index(request):
    symptoms_history = SymptomsLog.objects.filter(user=request.user)
    if request.method == "POST":
        symptom_name = request.POST["symptom_name"]
        # datetime from form is in iso format
        log_datetime_iso = request.POST["symptom-log-datetime"]
        utc_offset = request.POST["symptom-log-utc-offset"]
        log_datetime = datetime.fromisoformat(log_datetime_iso)
        # add utc offset to get the datetime in utc
        # because log_datetime is in user's local timezone
        log_datetime_utc = log_datetime + timedelta(minutes=int(utc_offset))
        # set tzinfo to make the datetime timezone aware
        log_datetime_utc = log_datetime_utc.replace(tzinfo=timezone.utc)
        # check if symptom_name already exists in db and get it if it does
        # or create a new Symptom if it does not exist
        try:
            symptom = Symptoms.objects.get(name=symptom_name)
        except Symptoms.DoesNotExist:
            symptom = Symptoms(name=symptom_name, added_by=request.user.username)
            symptom.save()
        new_log = SymptomsLog(
            datetime=log_datetime_utc,
            symptom=symptom,
            user = request.user,
        )
        new_log.save()
        return HttpResponseRedirect(reverse("symptoms:index"))

    return render(request, "symptoms/index.html", {
        "symptoms_history": symptoms_history,
    })


@login_required
def autocomplete_symptoms(request):
    """
    Provides autocomplete suggestions for symptom logging
    """
    # only allow ajax requests
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponseForbidden("403 Forbidden")
    query = request.GET.get("term", "")
    suggested_symptoms = list(Symptoms.objects.filter(
        (Q(added_by=request.user) | Q(added_by="admin(medlineplus)"))
         & Q(name__contains=query)
    ).values("name", "added_by"))
    # sort the suggestions so that the symptoms added by the user will always
    # be at the top and then it will be sorted by length which will result
    # in exact matches to the search term showing up at the top
    sorted_suggestions = sorted(
        suggested_symptoms, key=lambda item: (
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

