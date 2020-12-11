# Simulated-Conversations


## Setup for dev

#### Prereqs 
- Python 3.6.12
- Some sort of python virtual environment software (I will be using virtualenv)
 
#### TLDR:
All dependencies will be managed via requirements.txt and virtual environments. So, once you pull in the repo, create a virtual environment (probably somewhere in the repo) and install all the dependencies found in requirements.txt. If you add dependencies to the project, make sure to update requirements.txt so that others can easily update their environments when they pull in your changes. 

#### Walk-through (kinda)
For a Mac/Linux user this might look something like this (Windows users use the comments to figure out how to perform equivalent actions on Windows): 
```sh
# Clone the repo... the following will only work if you have GitHub set up with ssh which is highly recommended.
git clone git@github.com:Likhovodov/Simulated-Conversations.git 

# Change into django project directory. (this is optional... you can create your virtual environment anywhere)
cd Simulated-Conversations/simcon_project

python3 --version			# Confirm that you are using Python 3.6.12
virtualenv -p python3 env		# Create virtual environment 'env' using python3 (which for me points to python 3.6.12)
source env/bin/activate			# Activate virtual environment
pip3 install -r requirements.txt	# Install all the project dependencies inside your virtual environment
```
The project should now be set up . To start the development server run:
```sh
python manage.py runserver		# 'manage.py' is inside Simulated-Conversations/simcon_project
```
Ignore unapplied migration messages. As of writing this walk-through, this is not something we need to worry about. 
You should now be able to access the site at  http://127.0.0.1:8000/

If you add new dependencies to the project, update requirements.txt. This can be done like so:
```sh
# This should take all the dependencies installed in the virtual environment and dump them into requirements.txt
pip3 freeze > requirements.txt
```

#### Making database migrations

If any changes have been made to models.py, then Django will suggest that you make migrations. This will essentially
synchronize the database with the model fields.

To do this, change into the project-level directory and run:
```sh
python manage.py makemigrations
python manage.py migrate
```