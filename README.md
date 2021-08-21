
# Todo App API - CSoC Dev Task 5

## Introduction

Todo API server made with Django Rest framework and heroku postgresql.


### Setting up the project

- Make sure `python3.8` and `pip` are installed. Install `pipenv` by running `pip install pipenv`.
- Install python dependencies using the command `pipenv install` Please use only pipenv for managing dependencies (Follow this [link](https://realpython.com/pipenv-guide/) if you are new to pipenv).
- To activate this project's virtualenv, run `pipenv shell`.
- Run `python manage.py migrate` to apply migrations.
- Start the development server using `python manage.py runserver`

### Testing the API

The API can be tested by running the Django server locally, going to the following url: [http://127.0.0.1:8000/](http://127.0.0.1:8000/), clicking the "Try it out" button after selecting the endpoint and finally executing it along with the Response Body (if required).

For testing the endpoints which require **Token** in the Authorization header, you can click on the "Authorize" button, write the Authorization token as  `Token <token>` (which you have obtained from the `auth/login/` endpoint) and finally click on "Authorize". Thereafter, all the requests made to any endpoint will have the Token in the Authorization Header.

