from .models import MyModel


def db_query_context_processor(request):
    """
    Performs a query
    """
    try:
        val = MyModel.objects.get(pk=1)
        return {}
    except MyModel.DoesNotExist:
        return {}
