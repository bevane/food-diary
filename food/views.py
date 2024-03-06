from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Food

# Create your views here.
def index(request):
    food = Food.objects.all()
    if request.method == "POST":
        food_name = request.POST["food_name"]
        return HttpResponseRedirect(reverse("index"))
    return render(request, "food/index.html")
