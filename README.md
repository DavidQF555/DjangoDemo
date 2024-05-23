# Course Enroll
A Django demo app that simulates a course enrollment board.

## Setup
After cloning/installing, run the following to install all necessary libraries with pip: 

`pip install -r requirements.txt`

Then, run the following to setup the tables:

`python3 manage.py migrate`

Finally, run the following to start the server:

`python3 manage.py runserver`

You can also create super users using:

`python3 manage.py createsuperuser`

## Usage
In the root directory, there is a list of all available courses. You can register/login and enroll in them. 

The admin board is available in the `/admin` directory for super users. 