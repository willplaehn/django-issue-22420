A project to serve as a starting point for reliably reproducing the error in Django issue 22420. Tested on Django 1.11.1 with Postgres 9.4.11, 2014 MacBook Air.

This project has a simple model `MyModel` and an added context_processor that performs a database query. The test case uses threading and `TransactionTestCase` to reproduce the following error when the test suite cleans up (session count varies):

    django.db.utils.OperationalError: database "test_my_postgres_db" is being accessed by other users
    DETAIL:  There are 8 other sessions using the database.

It doesn't matter if an instance of the model exists or not (see `concurrency.migrations.0001_initial.py`), or if the connections cleanup decorator workaround from 22420 is added (see `concurrency.tests.py`).

Just run `python manage.py test` to reproduce!
