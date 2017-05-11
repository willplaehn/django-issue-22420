import threading

from django.db import connections
from django.test import RequestFactory, TransactionTestCase
from django.shortcuts import render


def test_concurrently(times):
    """
    Add this decorator to small pieces of code that you want to test
    concurrently to make sure they don't raise exceptions when run at the
    same time.  E.g., some Django views that do a SELECT and then a subsequent
    INSERT might fail when the INSERT assumes that the data has not changed
    since the SELECT.

    https://www.caktusgroup.com/blog/2009/05/26/testing-django-views-for-concurrency-issues/
    """
    def test_concurrently_decorator(test_func):
        def wrapper(*args, **kwargs):
            exceptions = []

            def call_test_func():
                try:
                    test_func(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    raise
            threads = []
            for i in range(times):
                threads.append(threading.Thread(target=call_test_func))
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            if exceptions:
                raise Exception('test_concurrently intercepted %s exceptions: %s' %
                                (len(exceptions), exceptions))
        return wrapper
    return test_concurrently_decorator


def close_db_connections(func, *args, **kwargs):
    """
    Decorator to explicitly close db connections during threaded execution

    Note this is necessary to work around:
    https://code.djangoproject.com/ticket/22420
    """
    def _close_db_connections(*args, **kwargs):
        ret = None
        try:
            ret = func(*args, **kwargs)
        finally:
            for conn in connections.all():
                conn.close()
        return ret
    return _close_db_connections


class ConcurrencyTest(TransactionTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    # @close_db_connections  # doesn't matter
    def test_add_dirs_render_override_with_concurrency(self):

        # @close_db_connections  # doesn't matter
        @test_concurrently(10)
        def get_response():
            request = self.factory.get('/my_path')
            render(request, 'index.html',)

        get_response()
