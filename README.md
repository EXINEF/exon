# unicam-project-group


To generate Django Class-Diagram use this command:
python manage.py graph_models -a -o myapp_models.png

To run the server:
python manage.py runserver

To run the tests:
python manage.py test

To run the tests with coverage:
python manage.py test --cov-report term-missing --cov-report html

To run the tests with coverage and profiling:
python manage.py test --cov-report term-missing --cov-report html --profile