from django.shortcuts import render
from django.db.models import Count
from symptoms.models import SymptomsLog
from food.models import Food,FoodLog
import pandas as pd

# Create your views here.
def index(request):
    symptoms_history = SymptomsLog.objects.filter(user=request.user)
    sym_count_per_date = symptoms_history.values("datetime__date").annotate(Count("id"))
    sym_count_per_date = list(sym_count_per_date)
    sym_data_x_values = [i["datetime__date"] for i in sym_count_per_date]
    sym_data_y_values = [i["id__count"] for i in sym_count_per_date]
    sym_data = [sym_data_x_values, sym_data_y_values]

    foods = Food.objects.all()
    food_history = FoodLog.objects.filter(user=request.user)

    # The food history data needs to be provided as 2 arrays
    # the first array is list of dates
    # the second array contains list of counts for each Food for the list of dates
    # pivot table function on pandas is used to generate the data according to the above
    # required format since sqlite does not have pivot queries
    foods_df = pd.DataFrame.from_records(foods.values())
    food_history_df = pd.DataFrame.from_records(food_history.values())
    food_data_df = (food_history_df.merge(foods_df, left_on="food_id", right_on="id", how="outer")
                                   .assign(date=lambda x: x["datetime"].dt.date)
                                   # assign a count of 1 for each row of food log
                                   # so that it can be summed later in pivot_table
                                   .assign(count=1)
                                   .pivot_table(index="date", columns="name",
                                                values="count", fill_value=0, aggfunc="sum")
    )
    food_data_x_values = food_data_df.index.values.tolist()
    food_data_y_values = food_data_df.to_dict(orient="list")
    food_data = [food_data_x_values, food_data_y_values]

    return render(request, "analyze/index.html", {
        "sym_data":sym_data,
        "food_data": food_data
    })
