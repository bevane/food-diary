"""
script to upload data from FoodData Central in the form of csv to webapp's
food db to make it easier for users to pick a food for their data entry
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas

load_dotenv('.env', override=True)

conn_string = os.environ.get("DATABASE_URL")
db = create_engine(conn_string)

# csv file downloaded from https://fdc.nal.usda.gov/download-datasets.html
# Full download of all datatypes
food_df = pandas.read_csv(
    "downloads/food.csv", usecols=["description", "data_type"],
    skip_blank_lines=True, 
)

# only select the below data types as these are the rows that contain
# the food names that will be most likely searched for by the user
food_df = (food_df.query('data_type in ["branded_food", "survey_fndds_food", "foundation_food"]')
           .drop(columns=["data_type"])
           .rename(columns={"description": "name"})
           # the food name constraint in webapp is 128 chars
           .query('name.str.len() <= 128')
           # differentiate between data added by this script and data added by
           # users etc.
           .assign(added_by="admin(fdc)")
           .drop_duplicates()
           .reset_index(drop=True)
)

with db.connect() as conn:
    # this method will only work for uploading fdc data for first time
    # because it will violate unique food "name" constraint if done a second
    # time. If fdc data in webapp needs to be updated
    # then delete all rows "added_by" "admin(fdc)" and rerun this script
    result = food_df.to_sql("food_food", con=conn, if_exists="append",
                            index=False)
    print(f"{result} rows added to food db")
