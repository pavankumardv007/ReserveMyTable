# BookmyTable

### Setup Instructions

1. Add the `.env` file for the project to the root folder , simialr to env.example 
2. `pipenv shell`
3. `pipenv install`
4. `python manage.py migrate`
5. `python manage.py runserver`

### for database changes

1. Make your changes
2. If database models were changed, run `python manage.py makemigrations` to migrate the project.
3. Apply database migrations using `python manage.py migrate` if necessary.
