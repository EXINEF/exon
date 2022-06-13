# EXON
This is the folder that contains the code of the web application that has been developed within the Project Course in Computer Science - CDT321 in MDU University.


To generate Django Class-Diagram use this command:
python manage.py graph_models -a -o myapp_models.png

To run the server locally:
python manage.py runserver

To run the tests:
python manage.py test

To run the tests with coverage:
python manage.py test --cov-report term-missing --cov-report html

To run the tests with coverage and profiling:
python manage.py test --cov-report term-missing --cov-report html --profile
