from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from .models import Symptoms, SymptomsLog
from datetime import datetime, timedelta, timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required
def index(request):
    registered_symptoms = list(Symptoms.objects.values_list("name", flat=True))
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
            symptom = Symptoms(name=symptom_name)
            symptom.save()
        new_log = SymptomsLog(
            datetime=log_datetime_utc,
            symptom=symptom,
            user = request.user,
        )
        new_log.save()
        return HttpResponseRedirect(reverse("symptoms:index"))

    return render(request, "symptoms/index.html", {
        "registered_symptoms": registered_symptoms,
        "symptoms_history": symptoms_history,
    })
