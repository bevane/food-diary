from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Food
from django.utils import timezone

# Create your views here.
def index(request):
    registered_foods = Food.objects.all()
    print(registered_foods)
    if request.method == "POST":
        food_name = request.POST["food_name"]
        new_food = Food(name=f"{food_name}")
        if not new_food.name.lower() in [food.name.lower() for food in registered_foods]:
            new_food.save()
        return HttpResponseRedirect(reverse("food:index"))
    
    current_datetime = timezone.now()
    current_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M")
    return render(request, "food/index.html", {
        "registered_foods": registered_foods,
        "current_datetime": current_datetime
    })
