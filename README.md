# 📑️ Food Diary

A django webapp to track relationship between foods eaten and symptoms experienced by the user.

Functionality:
- Food: Make food entries with name of food and timestamp
- Symptoms: Make symptom entries with name of symptom and timestamp
- Analyze: Visualize trends in food consumption and symptoms on a day to day basis

# Why?

Usually reactions to certain foods is very obvious (ex: allergic reactions) for many people.
More complex cases would require keeping a traditional food diary i.e. writing down what 
one eats and then observing the onset of any symptoms and then reading the food diary to identify 
any causes.

The act of keeping a traditional food diary can become tedious, especially for those who are 
forgetful. Journal/notes apps can help a bit but the user still has to identify correlations 
by just going through days and days worth of written 
information. Especially for more evasive complicated cases, using a food diary to identify
any correlations can lead to a lot of work and frustration for the user.

The Food Diary app aims to alleviate this issue by:
1. Providing a dedicated and easy-to-use interface for the user to make food and symptom entries
along with timestamps
2. Providing charts and basic analytics for the user to quickly identify any correlation
by observing trends in the foods they eat and symptoms they experience

# ⚙️ Development Build/Installation
**Python version: 3.11**

1. Clone the repo
2. cd to local repo
3. Optional: Highly recommended to set up python virtual environment:
    1. python3.11 -m venv .venv
    2. source .venv/bin/activate
4. `pip install -r requirements.txt` *recommended to set up a python virtual environment in repo directory beforehand*
5. `python manage.py migrate` to initialize the local db
6. `python manage.py createsuperuser` to create an admin account for yourself
7. `python manage.py runserver`
8. Once the server is running, open the domain provided (default: http://127.0.0.1:8000/). Sign in with superuser credentials to begin using the app
9. Currently, creation of additional user accounts can only be done by the admin: go to users in the admin page (http://127.0.0.1:8000/admin) and click add user
 
# Contribution
As this is a personal project of mine, I am not accepting any contributions at the moment. Though, feel free to fork the repo and try it out. Also I would be glad to receive any constructive criticism and feedback