from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Count
from symptoms.models import SymptomsLog
from django.core import serializers

# Create your views here.
def index(request):
    symptoms_history = SymptomsLog.objects.filter(user=request.user)
    count_per_date = symptoms_history.values("datetime__date").annotate(Count("id"))
    count_per_date = list(count_per_date)

    data_dates = [i["datetime__date"] for i in count_per_date]
    data_id_counts = [i["id__count"] for i in count_per_date]
    data = [data_dates, data_id_counts]

    return render(request, "analyze/index.html", {
        "data":data
    })
